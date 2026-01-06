#!/usr/bin/env python3
"""CERES arbitration CI fallback.

Mirrors validate-arbitration-ci.sh as of 85006775d8fe00470c49804eedede96817fce841.
Fallback only; shell remains authoritative.
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent


def run_or_exit(cmd: List[str], **kwargs) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(cmd, **kwargs)
    except FileNotFoundError:
        sys.stderr.write(f"{cmd[0]}: command not found\n")
        sys.exit(127)
    if result.returncode != 0:
        sys.exit(result.returncode)
    return result


def has_planner_files(directory: Path) -> bool:
    return all((directory / name).is_file() for name in ("task_graph.json", "concept_map.json", "required_syncs.json"))


def load_excludes() -> List[str]:
    excludes: List[str] = []
    repos = ROOT / "repos.yaml"
    if repos.is_file():
        for line in repos.read_text(encoding="utf-8").splitlines():
            if "local_path:" in line:
                parts = line.strip().split()
                if len(parts) == 2 and parts[0] == "local_path:":
                    excludes.append(parts[1])
    return excludes


def find_planner_dir() -> Optional[Path]:
    env_dir = os.getenv("ARBITRATION_PLANNER_DIR")
    if env_dir:
        candidate = Path(env_dir).expanduser().resolve()
        if not candidate.is_dir():
            sys.stderr.write(f"ARBITRATION_PLANNER_DIR is not a directory: {env_dir}\n")
            sys.exit(1)
        if not has_planner_files(candidate):
            sys.stderr.write(f"ARBITRATION_PLANNER_DIR missing required planner artifacts: {candidate}\n")
            sys.exit(1)
        return candidate

    excludes = set([".git", "node_modules"] + load_excludes())
    candidates: List[Path] = []

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in excludes]
        if "task_graph.json" in files:
            directory = Path(root)
            if has_planner_files(directory):
                candidates.append(directory)

    unique = sorted({str(path) for path in candidates})
    if len(unique) > 1:
        sys.stderr.write("Multiple planner output directories detected; set ARBITRATION_PLANNER_DIR to disambiguate:\n")
        for item in unique:
            sys.stderr.write(f"  - {item}\n")
        sys.exit(1)
    if len(unique) == 1:
        return Path(unique[0])
    return None


def build_arbitration_input(planner_dir: Path, output_path: Path) -> None:
    task_graph = json.loads((planner_dir / "task_graph.json").read_text(encoding="utf-8"))
    concept_map = json.loads((planner_dir / "concept_map.json").read_text(encoding="utf-8"))
    required_syncs = json.loads((planner_dir / "required_syncs.json").read_text(encoding="utf-8"))

    task_concept: Dict[str, str] = {}
    for entry in concept_map.get("tasks", []) or []:
        if entry and entry.get("task_id") and entry.get("concept"):
            task_concept[str(entry["task_id"])] = str(entry["concept"])

    depends_on_by_task: Dict[str, set] = {}
    concept_deps_by_task: Dict[str, set] = {}

    for edge in task_graph.get("edges", []) or []:
        if not edge or edge.get("from") is None or edge.get("to") is None:
            continue
        from_id = str(edge["from"])
        to_id = str(edge["to"])
        depends_on_by_task.setdefault(to_id, set()).add(from_id)

        from_concept = task_concept.get(from_id)
        to_concept = task_concept.get(to_id)
        if from_concept and to_concept and from_concept != to_concept:
            concept_deps_by_task.setdefault(to_id, set()).add(from_concept)

    tasks: List[Dict[str, Any]] = []
    for task in task_graph.get("tasks", []) or []:
        task_id = str(task.get("task_id", ""))
        entry: Dict[str, Any] = {
            "id": task_id,
            "concept": task_concept.get(task_id),
            "type": task.get("type"),
            "priority": task.get("priority"),
            "timestamp": task.get("timestamp"),
            "depends_on": sorted(depends_on_by_task.get(task_id, set())),
        }
        concept_deps = sorted(concept_deps_by_task.get(task_id, set()))
        if concept_deps:
            entry["concept_dependencies"] = concept_deps
        entry = {key: value for key, value in entry.items() if value is not None}
        tasks.append(entry)

    tasks.sort(key=lambda item: item.get("id", ""))

    concepts = sorted(
        {str(entry.get("concept")) for entry in concept_map.get("tasks", []) or [] if entry.get("concept")}
    )

    syncs = [
        {
            "name": str(sync.get("sync_id")),
            "from": str(sync.get("from_concept")),
            "to": str(sync.get("to_concept")),
        }
        for sync in required_syncs.get("synchronizations", []) or []
    ]
    syncs.sort(key=lambda item: item.get("name", ""))

    payload = {
        "concepts": concepts,
        "synchronizations": syncs,
        "tasks": tasks,
    }

    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def stable_stringify(value: Any) -> str:
    if isinstance(value, list):
        return "[" + ",".join(stable_stringify(item) for item in value) + "]"
    if isinstance(value, dict):
        keys = sorted(value.keys())
        return "{" + ",".join(f"{json.dumps(key)}:{stable_stringify(value[key])}" for key in keys) + "}"
    return json.dumps(value)


def sanitize_output(output: Dict[str, Any]) -> Dict[str, Any]:
    clone = json.loads(json.dumps(output))
    decision_log = clone.get("decision_log")
    if isinstance(decision_log, dict):
        decision_log.pop("generated_at", None)
    return clone


def main() -> None:
    arbitrator = ROOT / "arbitration" / "arbitrator.js"
    if not arbitrator.is_file():
        sys.stderr.write(f"Arbitration engine not found: {arbitrator}\n")
        sys.exit(1)

    planner_dir = find_planner_dir()

    logs_dir = ROOT / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    out_primary = logs_dir / "arbitration-decision.json"
    out_second = logs_dir / "arbitration-decision-second.json"

    if planner_dir:
        validator = ROOT / "planner" / "planner-output-validator.js"
        if not validator.is_file():
            sys.stderr.write(f"Planner output validator not found: {validator}\n")
            sys.exit(1)

        print(f"Planner output detected: {planner_dir}")
        run_or_exit(["node", str(validator), "--dir", str(planner_dir)])

        input_path = logs_dir / "arbitration-input.json"
        build_arbitration_input(planner_dir, input_path)
    else:
        input_path = ROOT / "templates" / "arbitration" / "fixture.json"
        sys.stderr.write("No planner output directory detected; using fixture input.\n")

    if not input_path.is_file():
        sys.stderr.write(f"Arbitration input not found: {input_path}\n")
        sys.exit(1)

    run_or_exit(["node", str(arbitrator), "--input", str(input_path), "--output", str(out_primary)])
    run_or_exit(["node", str(arbitrator), "--input", str(input_path), "--output", str(out_second)])

    output_a = json.loads(out_primary.read_text(encoding="utf-8"))
    output_b = json.loads(out_second.read_text(encoding="utf-8"))

    if output_a.get("status") != "ok":
        sys.stderr.write(f"Arbitration failed: status={output_a.get('status')}\n")
        blocked = output_a.get("blocked")
        if isinstance(blocked, list) and blocked:
            task_ids = ", ".join(item.get("task_id", "") for item in blocked)
            sys.stderr.write(f"Blocked tasks: {task_ids}\n")
        sys.exit(1)

    hash_a = stable_stringify(sanitize_output(output_a))
    hash_b = stable_stringify(sanitize_output(output_b))

    if hash_a != hash_b:
        sys.stderr.write("Determinism check failed: arbitration outputs differ between runs.\n")
        sys.exit(1)

    sys.stdout.write(out_primary.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()

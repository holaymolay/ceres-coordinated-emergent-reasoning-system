#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = REPO_ROOT / "artifacts"


def run_cmd(cmd: list[str], cwd: Path, env: Optional[Dict[str, str]] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        text=True,
        capture_output=True,
        env=env or os.environ.copy(),
    )


def clone_repo(tmp_root: Path) -> Path:
    repo_path = tmp_root / "repo"
    subprocess.run(
        ["git", "clone", "--local", str(REPO_ROOT), str(repo_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return repo_path


def reset_repo(repo_path: Path) -> None:
    subprocess.run(
        ["git", "reset", "--hard"],
        cwd=repo_path,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    subprocess.run(
        ["git", "clean", "-fdx"],
        cwd=repo_path,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def append_line(path: Path, line: str) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"{line}\n")


def expect_failure(result: subprocess.CompletedProcess) -> tuple[bool, str]:
    output = (result.stderr or "") + (result.stdout or "")
    output = output.strip()
    if result.returncode == 0:
        return False, output
    if not output or "ERROR" not in output:
        return False, output
    return True, output


def test_multi_concept(repo_path: Path) -> subprocess.CompletedProcess:
    concept_a = repo_path / "concepts" / "ui-intent-protocol" / "README.md"
    append_line(concept_a, "temp multi-concept change")
    concept_b = repo_path / "concepts" / "alpha"
    concept_b.mkdir(parents=True, exist_ok=True)
    append_line(concept_b / "note.txt", "temp concept change")
    return run_cmd(["scripts/check-invariants.sh"], repo_path)


def test_dirty_git_tree(repo_path: Path) -> subprocess.CompletedProcess:
    append_line(repo_path / "dirty.txt", "temp")
    return run_cmd(["scripts/check-git-state.sh"], repo_path)


def test_missing_dod(repo_path: Path) -> subprocess.CompletedProcess:
    append_line(repo_path / "scripts" / "temp-change.txt", "temp")
    return run_cmd(["scripts/check-invariants.sh"], repo_path)


def test_missing_run_receipt(repo_path: Path) -> subprocess.CompletedProcess:
    append_line(repo_path / "scripts" / "temp-change.txt", "temp")
    append_line(repo_path / "completed.md", "- [x] temp completion entry")
    append_line(repo_path / "handover.md", "- temp handover entry")
    append_line(repo_path / "CHANGELOG.md", "## 2000-01-01T00:00:00+00:00\n- temp")
    return run_cmd(["scripts/check-invariants.sh"], repo_path)


def test_fast_mode_boundary(repo_path: Path) -> subprocess.CompletedProcess:
    scope = "fast-mode-test"
    append_line(repo_path / "todo.md", f"- [ ] {scope}")
    append_line(repo_path / "handover.md", f"Fast Mode: {scope}")
    append_line(repo_path / "docs/context/planner-task-manager.md", f"Fast Mode scope: {scope}")
    append_line(repo_path / "concepts" / "ui-intent-protocol" / "README.md", "temp fast mode change")
    concept_b = repo_path / "concepts" / "alpha"
    concept_b.mkdir(parents=True, exist_ok=True)
    append_line(concept_b / "note.txt", "temp concept change")
    env = os.environ.copy()
    env["EXECUTION_PROFILE"] = "FAST"
    env["FAST_MODE_SCOPE"] = scope
    return run_cmd(["scripts/check-invariants.sh"], repo_path, env=env)


def main() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    audit_date = datetime.utcnow().strftime("%Y-%m-%d")
    artifact_path = ARTIFACTS_DIR / f"enforcement-audit-{audit_date}.json"

    tests = [
        {
            "name": "multi-concept-modification",
            "script": "scripts/check-invariants.sh",
            "runner": test_multi_concept,
        },
        {
            "name": "dirty-git-tree",
            "script": "scripts/check-git-state.sh",
            "runner": test_dirty_git_tree,
        },
        {
            "name": "missing-dod-artifacts",
            "script": "scripts/check-invariants.sh",
            "runner": test_missing_dod,
        },
        {
            "name": "missing-run-receipt-safe-mode",
            "script": "scripts/check-invariants.sh",
            "runner": test_missing_run_receipt,
        },
        {
            "name": "fast-mode-boundary-violation",
            "script": "scripts/check-invariants.sh",
            "runner": test_fast_mode_boundary,
        },
    ]

    results = []
    overall_pass = True

    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = clone_repo(Path(tmpdir))
        for test in tests:
            result = test["runner"](repo_path)
            passed, output = expect_failure(result)
            actual = "fail" if result.returncode != 0 else "pass"
            results.append(
                {
                    "test_name": test["name"],
                    "expected_outcome": "fail",
                    "actual_outcome": actual,
                    "pass": passed,
                    "enforcement_script": test["script"],
                    "message": output,
                }
            )
            if not passed:
                overall_pass = False
            reset_repo(repo_path)

    payload = {
        "date": audit_date,
        "tests": results,
    }
    artifact_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

    if not overall_pass:
        print(f"Enforcement audit failed. See {artifact_path}")
        raise SystemExit(1)
    print(f"Enforcement audit passed. See {artifact_path}")


if __name__ == "__main__":
    main()

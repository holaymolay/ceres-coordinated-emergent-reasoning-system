#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable

from uip_yaml import YamlError, load_yaml


PHASE_SIDE_EFFECTS = {"allowed", "forbidden"}
PHASE_MEMORY_SCOPE = {"draft", "working", "readonly"}


def fail(message: str) -> None:
    sys.stderr.write(f"ERROR: {message}\n")
    sys.exit(1)


def load_yaml_file(path: Path, label: str) -> Any:
    if not path.exists():
        fail(f"{label} not found: {path}")
    try:
        return load_yaml(path)
    except YamlError as exc:
        fail(f"{label} YAML error: {exc}")
    return None


def load_json_file(path: Path, label: str) -> Any:
    if not path.exists():
        fail(f"{label} not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"{label} JSON error: {exc}")
    return None


def require_list(value: Any, label: str) -> list:
    if not isinstance(value, list):
        fail(f"{label} must be a list")
    return value


def require_dict(value: Any, label: str) -> dict:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    return value


def as_str(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{label} must be a non-empty string")
    return value.strip()


def validate_inference_phases(path: Path) -> dict:
    data = require_dict(load_yaml_file(path, "Inference phase model"), "Inference phase model")
    phases = require_list(data.get("phases"), "Inference phase model phases")
    phase_map: Dict[str, dict] = {}
    for idx, phase in enumerate(phases, start=1):
        phase = require_dict(phase, f"Phase {idx}")
        name = as_str(phase.get("name"), f"Phase {idx} name")
        allowed_agents = require_list(phase.get("allowed_agents"), f"Phase {name} allowed_agents")
        side_effects = as_str(phase.get("side_effects"), f"Phase {name} side_effects")
        memory_scope = as_str(phase.get("memory_scope"), f"Phase {name} memory_scope")

        if side_effects not in PHASE_SIDE_EFFECTS:
            fail(f"Phase {name} side_effects must be one of {sorted(PHASE_SIDE_EFFECTS)}")
        if memory_scope not in PHASE_MEMORY_SCOPE:
            fail(f"Phase {name} memory_scope must be one of {sorted(PHASE_MEMORY_SCOPE)}")

        phase_map[name] = {
            "name": name,
            "allowed_agents": [as_str(agent, f"Phase {name} allowed_agent") for agent in allowed_agents],
            "side_effects": side_effects,
            "memory_scope": memory_scope,
        }

    requires_reflection = data.get("requires_reflection_for", [])
    if requires_reflection and not isinstance(requires_reflection, list):
        fail("requires_reflection_for must be a list if provided")

    return {
        "phases": phase_map,
        "requires_reflection_for": [str(item) for item in requires_reflection],
    }


def validate_agents(path: Path) -> dict:
    data = require_dict(load_yaml_file(path, "AGENTS registry"), "AGENTS registry")
    patterns = require_list(data.get("patterns"), "AGENTS patterns")
    pattern_set = {as_str(item, "pattern") for item in patterns}

    agents = require_list(data.get("agents"), "AGENTS registry agents")
    agent_map: Dict[str, dict] = {}
    for idx, agent in enumerate(agents, start=1):
        agent = require_dict(agent, f"Agent {idx}")
        name = as_str(agent.get("name"), f"Agent {idx} name")
        supports = require_list(agent.get("supports_patterns"), f"Agent {name} supports_patterns")
        allowed_phases = require_list(agent.get("allowed_phases"), f"Agent {name} allowed_phases")
        side_effects = as_str(agent.get("side_effects"), f"Agent {name} side_effects")

        if side_effects not in PHASE_SIDE_EFFECTS:
            fail(f"Agent {name} side_effects must be one of {sorted(PHASE_SIDE_EFFECTS)}")

        supports_clean = [as_str(item, f"Agent {name} supports_patterns") for item in supports]
        for item in supports_clean:
            if item not in pattern_set:
                fail(f"Agent {name} supports unknown pattern: {item}")

        agent_map[name] = {
            "name": name,
            "role": agent.get("role"),
            "supports_patterns": supports_clean,
            "allowed_phases": [as_str(item, f"Agent {name} allowed_phase") for item in allowed_phases],
            "side_effects": side_effects,
        }

    return {"agents": agent_map, "patterns": pattern_set}


def validate_agent_phase(phase: str, agent: str, pattern: str | None, phases: dict, agents: dict) -> None:
    if phase not in phases:
        fail(f"Phase not defined: {phase}")
    if agent not in agents:
        fail(f"Agent not defined: {agent}")

    phase_cfg = phases[phase]
    agent_cfg = agents[agent]

    if agent not in phase_cfg["allowed_agents"]:
        fail(f"Agent {agent} not allowed in phase {phase}")
    if phase not in agent_cfg["allowed_phases"]:
        fail(f"Agent {agent} not permitted for phase {phase} per AGENTS")

    if pattern:
        if pattern not in agent_cfg["supports_patterns"]:
            fail(f"Agent {agent} does not support pattern {pattern}")


def ensure_known_keys(payload: dict, allowed: Iterable[str], label: str) -> None:
    allowed_set = set(allowed)
    for key in payload.keys():
        if key not in allowed_set:
            fail(f"{label} has unknown key: {key}")


def validate_synchronizations(sync_dir: Path) -> None:
    if not sync_dir.exists():
        return
    allowed_keys = {"name", "from", "to", "direction", "concepts", "allow_cycle", "message_contract"}
    for path in sorted(sync_dir.glob("*.yaml")):
        data = require_dict(load_yaml_file(path, f"Synchronization {path}"), f"Synchronization {path}")
        ensure_known_keys(data, allowed_keys, f"Synchronization {path}")

        name = data.get("name")
        as_str(name, f"Synchronization name in {path}")

        has_from_to = "from" in data or "to" in data
        has_direction = "direction" in data or "concepts" in data

        if has_from_to and has_direction:
            fail(f"Synchronization {path} cannot mix from/to with direction/concepts")
        if not has_from_to and not has_direction:
            fail(f"Synchronization {path} must define from/to or direction/concepts")

        if has_from_to:
            as_str(data.get("from"), f"Synchronization from in {path}")
            as_str(data.get("to"), f"Synchronization to in {path}")
        else:
            direction = as_str(data.get("direction"), f"Synchronization direction in {path}")
            if direction != "bidirectional":
                fail(f"Synchronization {path} direction must be 'bidirectional'")
            concepts = require_list(data.get("concepts"), f"Synchronization concepts in {path}")
            if len(concepts) < 2:
                fail(f"Synchronization {path} concepts must include at least 2 items")
            for item in concepts:
                as_str(item, f"Synchronization concept in {path}")

        if "allow_cycle" in data and not isinstance(data.get("allow_cycle"), bool):
            fail(f"Synchronization {path} allow_cycle must be boolean")

        if "message_contract" in data:
            mc = require_dict(data.get("message_contract"), f"message_contract in {path}")
            ensure_known_keys(mc, {"input_schema", "output_schema", "transport"}, f"message_contract in {path}")
            as_str(mc.get("input_schema"), f"message_contract.input_schema in {path}")
            as_str(mc.get("output_schema"), f"message_contract.output_schema in {path}")
            transport = as_str(mc.get("transport"), f"message_contract.transport in {path}")
            if transport not in {"internal", "mcp", "external"}:
                fail(f"message_contract.transport in {path} must be internal, mcp, or external")


def validate_record_types(record: dict, properties: dict, required: list[str], label: str) -> None:
    for key in required:
        if key not in record:
            fail(f"{label} missing required field: {key}")
    for key, value in record.items():
        if key not in properties:
            fail(f"{label} has unknown field: {key}")
        spec = properties[key]
        expected = spec.get("type")
        if expected == "string" and not isinstance(value, str):
            fail(f"{label} field {key} must be string")
        if expected == "integer" and not isinstance(value, int):
            fail(f"{label} field {key} must be integer")
        if expected == "object" and not isinstance(value, dict):
            fail(f"{label} field {key} must be object")
        if expected == "array" and not isinstance(value, list):
            fail(f"{label} field {key} must be array")
        if "enum" in spec and value not in spec.get("enum", []):
            fail(f"{label} field {key} must be one of {spec.get('enum')}")


def validate_memory_records(memory_dir: Path, schema_path: Path) -> None:
    if not memory_dir.exists():
        return
    schema = load_json_file(schema_path, "Memory record schema")
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    for path in sorted(memory_dir.glob("*.json")):
        record = load_json_file(path, f"Memory record {path}")
        record = require_dict(record, f"Memory record {path}")
        validate_record_types(record, properties, required, f"Memory record {path}")


def validate_observability_events(events_path: Path, schema_path: Path) -> None:
    if not events_path.exists():
        return
    schema = load_json_file(schema_path, "Observability event schema")
    properties = schema.get("properties", {})
    required = schema.get("required", [])

    for line_no, raw in enumerate(events_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(f"Observability event JSON error at line {line_no}: {exc}")
        event = require_dict(event, f"Observability event line {line_no}")
        validate_record_types(event, properties, required, f"Observability event line {line_no}")


def find_reflection_event(events_path: Path, task_id: str) -> bool:
    if not events_path.exists():
        return False
    for raw in events_path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        if event.get("type") != "critique":
            continue
        if event.get("phase") != "reflection":
            continue
        if event.get("task_id") == task_id:
            return True
        context = event.get("context")
        if isinstance(context, dict) and context.get("task_id") == task_id:
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate CERES governance contracts")
    parser.add_argument("--hub-root", type=Path, help="Path to CERES hub root")
    parser.add_argument("--phase", help="Active phase name")
    parser.add_argument("--agent", help="Active agent name")
    parser.add_argument("--pattern", help="Active pattern name")
    parser.add_argument("--task-class", help="Task class (e.g., codegen, migration, security)")
    parser.add_argument("--task-id", help="Task identifier for reflection checks")
    parser.add_argument("--events", type=Path, help="Observability events file")
    args = parser.parse_args()

    hub_root = args.hub_root
    if hub_root is None:
        hub_root = Path(__file__).resolve().parents[2]
    hub_root = hub_root.resolve()

    phases_path = hub_root / "governance" / "inference-phases.yaml"
    agents_path = hub_root / "AGENTS.md"
    sync_dir = hub_root / "synchronizations"
    memory_dir = hub_root / "memory" / "records"
    events_path = args.events or (hub_root / "logs" / "events.jsonl")

    sync_schema = hub_root / "schemas" / "synchronization.schema.json"
    memory_schema = hub_root / "schemas" / "memory-record.schema.json"
    observability_schema = hub_root / "schemas" / "observability-event.schema.json"

    phases = validate_inference_phases(phases_path)
    agents = validate_agents(agents_path)

    if args.phase and args.agent:
        validate_agent_phase(args.phase, args.agent, args.pattern, phases["phases"], agents["agents"])

    validate_synchronizations(sync_dir)
    validate_memory_records(memory_dir, memory_schema)
    validate_observability_events(events_path, observability_schema)

    if args.task_class and args.task_class in phases.get("requires_reflection_for", []):
        if args.phase in {"execution", "correction"}:
            if not args.task_id:
                fail("task_id required to enforce reflection for task class")
            if not find_reflection_event(events_path, args.task_id):
                fail("Reflection required but no critique event found for task")

    sys.stdout.write("Governance contracts validated\n")


if __name__ == "__main__":
    main()

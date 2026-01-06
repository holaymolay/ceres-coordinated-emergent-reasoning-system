# Planner Output Standardization

This defines the canonical, machine-auditable planner outputs required by CERES. Planning MUST complete successfully before arbitration or execution.

## Required Planner Output Artifacts

Planners must emit exactly three files:
- `task_graph.json`
- `concept_map.json`
- `required_syncs.json`

Schemas:
- `schemas/task_graph.schema.json`
- `schemas/concept_map.schema.json`
- `schemas/required_syncs.schema.json`

## Validator

Use `planner/planner-output-validator.js` to validate a planner output directory:

```bash
node planner/planner-output-validator.js --dir path/to/planner-output
```

The validator rejects outputs if:
- A task maps to multiple Concepts.
- Dependencies are implicit or undeclared (task depends_on not represented in edges).
- Cross-Concept edges are missing required Synchronizations.
- The task graph is not a DAG.

## Example Valid Output

`task_graph.json`
```json
{
  "tasks": [
    {
      "task_id": "t-001",
      "description": "Define governance contract",
      "type": "planning",
      "priority": "high",
      "timestamp": "2024-12-01T10:00:00Z"
    },
    {
      "task_id": "t-002",
      "description": "Apply lifecycle gate",
      "type": "validation",
      "priority": 60,
      "timestamp": "2024-12-01T10:05:00Z",
      "depends_on": ["t-001"]
    }
  ],
  "edges": [
    { "from": "t-001", "to": "t-002" }
  ]
}
```

`concept_map.json`
```json
{
  "tasks": [
    { "task_id": "t-001", "concept": "governance" },
    { "task_id": "t-002", "concept": "runtime" }
  ]
}
```

`required_syncs.json`
```json
{
  "synchronizations": [
    {
      "sync_id": "governance-to-runtime",
      "from_concept": "governance",
      "to_concept": "runtime",
      "status": "existing",
      "reason": "Planner dependency t-001 -> t-002"
    }
  ]
}
```

## Example Invalid Output (With Error Explanation)

`task_graph.json`
```json
{
  "tasks": [
    { "task_id": "t-001", "description": "Draft objective" },
    { "task_id": "t-002", "description": "Execute" }
  ],
  "edges": [
    { "from": "t-001", "to": "t-002" }
  ]
}
```

`concept_map.json`
```json
{
  "tasks": [
    { "task_id": "t-001", "concept": "governance" },
    { "task_id": "t-001", "concept": "runtime" },
    { "task_id": "t-002", "concept": "runtime" }
  ]
}
```

`required_syncs.json`
```json
{ "synchronizations": [] }
```

Errors produced:
- Task `t-001` mapped to multiple Concepts (violates single‑Concept constraint).
- Cross‑Concept edge `t-001`(governance) → `t-002`(runtime) missing required Synchronization.

## Why This Prevents Drift

A fixed output schema forces planning to be explicit, deterministic, and auditable. It removes ambiguity about task ownership, execution ordering, and cross‑Concept boundaries, which in turn makes arbitration and execution reliable and replayable.

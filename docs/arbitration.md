# Deterministic Arbitration Rules (CERES)

This defines a deterministic arbitration model that orders, accepts, or rejects tasks when multiple agents compete for execution. The arbitration engine is a standalone service located at `arbitration/arbitrator.js`.

## Arbitration Rules (Ordered)

1. **Normalize task fields**
   - Required inputs: `id`, `concept`, `type`, `priority` (explicit or inferred), `timestamp`.
   - `type` is normalized to `planning | validation | execution`.
   - `priority` is inferred if missing using fixed type weights.

2. **Validate required fields**
   - Reject tasks missing `concept`, valid `type`, or a parseable `timestamp`.

3. **Validate Concept ownership**
   - If a Concept registry exists (from `concepts/` or input), reject tasks whose `concept` is unknown.

4. **Validate Synchronizations**
   - If Synchronizations exist (from `synchronizations/` or input), reject tasks that:
     - Reference unknown Synchronizations, or
     - Declare a Synchronization that does not include the task’s `concept`, or
     - Declare Concept dependencies without a matching Synchronization.

5. **Validate task dependencies**
   - Reject tasks that depend on unknown task IDs.

6. **Deterministic ordering**
   - Sort accepted tasks by:
     1) Priority (desc)
     2) Task type (planning > validation > execution)
     3) Timestamp (asc)
     4) Concept name (asc)
     5) Task ID (asc)

7. **Concept serialization**
   - Tasks touching the same Concept are serialized in the order above (no parallel execution within a Concept).

## Determinism Guarantees

- The engine sorts tasks using a fixed comparator and stable tie‑breakers.
- The decision log includes an input digest and rule trace, so the same input yields the same output.
- No randomness, external services, or mutable state is used.

## Example Input → Output Trace

Input (`tasks.json`):
```json
{
  "tasks": [
    {
      "id": "t-001",
      "concept": "governance",
      "type": "planning",
      "priority": "high",
      "timestamp": "2024-12-01T10:00:00Z"
    },
    {
      "id": "t-002",
      "concept": "governance",
      "type": "execution",
      "priority": 50,
      "timestamp": "2024-12-01T10:05:00Z"
    },
    {
      "id": "t-003",
      "concept": "runtime",
      "type": "validation",
      "priority": 60,
      "timestamp": "2024-12-01T10:02:00Z"
    }
  ]
}
```

Output (excerpt):
```json
{
  "status": "ok",
  "order": ["t-001", "t-003", "t-002"],
  "accepted": [
    { "task_id": "t-001", "concept": "governance", "type": "planning", "priority": 75 },
    { "task_id": "t-003", "concept": "runtime", "type": "validation", "priority": 60 },
    { "task_id": "t-002", "concept": "governance", "type": "execution", "priority": 50 }
  ]
}
```

## How To Run

```bash
node arbitration/arbitrator.js --input tasks.json --output arbitration-decision.json
```

The engine emits a structured decision log that is replayable and auditable.

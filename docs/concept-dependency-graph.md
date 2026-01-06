# Concept Dependency Graph Validation

This validator builds a canonical Concept Dependency Graph from manifests and Synchronization declarations, then enforces strict cross-Concept governance rules.

## Graph Construction
- **Nodes**: Concepts in `concepts/<concept_name>/`.
- **Edges**: Directed edges from `synchronizations/*.yaml`.

The graph is built by reading:
- `concepts/<concept_name>/manifest.yaml`
- `synchronizations/*.yaml`

## Manifest Fields Used
Each Concept manifest should declare dependencies and Synchronizations:

```yaml
dependencies:
  read:
    - concept-a
  write:
    - concept-b
synchronizations:
  outgoing:
    - sync-a-to-b
  incoming:
    - sync-b-to-a
```

## Synchronization Fields Used
Each Synchronization file should declare its endpoints and any cycle allowance:

```yaml
name: sync-a-to-b
from: concept-a
to: concept-b
allow_cycle: false
```

Optional bidirectional form:

```yaml
name: sync-a-b
direction: bidirectional
concepts: [concept-a, concept-b]
allow_cycle: true
```

## Guarantees Enforced
- No implicit dependencies: every dependency must be backed by a Synchronization.
- No orphaned Synchronizations: every sync must point to existing Concepts.
- Manifests must declare their incoming/outgoing Synchronizations.
- Cycles are forbidden unless all edges in the cycle are explicitly marked `allow_cycle: true`.

## How to Run
```bash
node scripts/validate-concept-graph.js
```

The validator exits non-zero on violations and prints human-readable errors with file paths for remediation.

## Governance Fit
This validator is a hard enforcement layer in CERES. It prevents cross-Concept coupling from becoming implicit and ensures all interactions remain explicit, reviewable, and contract-driven.

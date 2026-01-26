# Prompt: Hard Iteration Contract Layer

Prompt ID: 447fffde-cbed-4783-a181-0b12b5fc8eff
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-26T07:22:29Z
Last-Modified: 2026-01-26T17:35:22Z

## Intent
Add an optional, removable Hard Iteration Contract utility that is deterministic, single-step, and off by default.

## Constraints
- Must be read-only with respect to governance authority: it may write artifacts, but may not mutate or gate existing CERES governance state or execution.
- Must be OFF by default. No background loops. No automatic runs.
- Must be fully removable: deleting the new files must not break existing CERES behavior.
- Must be deterministic: given the same inputs, it produces the same "next task" recommendation and the same artifacts.
- Must not introduce any self-expanding behavior, hidden agency, or autonomous continuation.

## Task Decomposition Guidance (decomposable only)
N/A

## Prompt Body
### Intent
Implement an OPTIONAL "Hard Iteration Contract" that tightens determinism/observability without changing any existing execution paths by default.

### Constraints
- Must be read-only with respect to governance authority: it may write artifacts, but may not mutate or gate existing CERES governance state or execution.
- Must be OFF by default. No background loops. No automatic runs.
- Must be fully removable: deleting the new files must not break existing CERES behavior.
- Must be deterministic: given the same inputs, it produces the same "next task" recommendation and the same artifacts.
- Must not introduce any self-expanding behavior, hidden agency, or autonomous continuation.

### Scope
Goal
Introduce a "single-step iteration ritual" that always emits the same minimal artifact set:
1) deterministically select exactly one next work item
2) record the selection + rationale
3) require/record acceptance criteria reference
4) attach/record evidence references (if any)
5) flip a local pass/fail flag for that item (local to this layer)
6) append a progress entry

Scope
Create a new optional utility under a new top-level (or existing appropriate) directory, e.g.:
- tools/iteration/ OR scripts/iteration/
- and a docs page.

Authoritative inputs (read-only)
- A local iteration backlog file (new) that this utility owns.
- Existing CERES artifacts may be referenced, but not modified.

New artifacts (owned by this layer)
1) scripts/iteration/backlog.json (or .yaml)
   - list of items with:
     id (string), priority (int), title, spec_ref (path or id), acceptance_criteria_ref (path or anchor), passes (bool), evidence_refs (array), created_at
   - semantics: this is NOT the CERES task system; it is an optional "iteration backlog" for the ritual.
2) scripts/iteration/progress.jsonl (append-only)
   - one entry per ritual run: timestamp, selected_id, inputs_hash, decision_rule_version, result (pass/fail/partial), evidence_refs, notes
3) scripts/iteration/README.md (format + rules)
4) docs/iteration-ritual.md (user-facing explanation + guarantees)

Deterministic selection rule
- Select the highest priority item where passes=false.
- Tie-breaker: lexicographic id ascending.
- Output must include the exact rule used and the computed ordering for the first N items (N=5) to ensure auditability.

CLI / entrypoint
Add a script (python preferred) that runs ONE iteration step:
- ceres-iterate (or scripts/iteration/run.py)
Behavior:
- Loads backlog
- Selects next item deterministically
- Emits a "selection record" to stdout
- Appends to progress.jsonl
- Optionally (flag) records evidence refs passed via CLI args
- Optionally (flag) toggles passes=true ONLY in backlog.json for that selected item (owned file), never elsewhere
- Never runs more than one step per invocation

Flags
- --backlog path (default scripts/iteration/backlog.json)
- --progress path (default scripts/iteration/progress.jsonl)
- --set-pass true|false (default false; if true sets passes=true for selected item ONLY)
- --evidence-ref <string> (repeatable)
- --dry-run (no writes)
- --show-order (prints top 5 ordered candidates)

Tests
Add minimal tests proving:
- Deterministic selection and tie-breaking.
- Dry-run performs zero writes.
- Writes are limited strictly to owned files.
- Removing the tool directory does not impact core CERES import paths/tests (add a simple parity test if your test harness supports it).

Documentation requirements
- docs/iteration-ritual.md must explicitly state:
  - OFF by default
  - single-step only
  - owned artifacts list
  - no governance authority
  - removability guarantee
  - deterministic rule
  - how to use and how to uninstall

Deliverables
- New tool + docs + tests committed.
- Do NOT refactor existing CERES layers.
- Keep changes atomic and isolated.

Start by inspecting the repo structure to choose the correct placement. Then implement files, CLI, and tests.

### Inputs
- Existing repo structure and tooling conventions.
- The owned artifacts defined in this prompt.

### Required Reasoning
- Keep changes isolated to the new iteration utility and its docs.
- Ensure writes are limited to owned artifacts and deterministic.

### Output Artifacts
- New optional iteration utility, docs, and tests as specified.
- Documented usage and uninstall steps in docs/iteration-ritual.md.

### Validation Criteria
- Deterministic selection and tie-breaking implemented.
- Dry-run performs zero writes.
- Writes limited strictly to owned files.
- Tool removal does not impact core CERES behavior.
- Documentation states off-by-default and removability guarantees.

## Validation Criteria
- All deliverables and validation criteria in the prompt body are satisfied.

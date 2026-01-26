# Prompt: Terminal-Bench Rigor Gates

Prompt ID: 3e7f9154-7136-48a9-8753-a633294843cf
Classification: decomposable
Status: draft
Owner: user
Created: 2026-01-26T07:18:50Z
Last-Modified: 2026-01-26T08:02:12Z

## Intent
Implement Terminal-Bench-derived rigor gates with the required artifacts, CLI, and tests under spec-first governance.

## Constraints
- Repo-local changes only (docs, schemas, templates, CLI integration, tests).
- Follow prompt-artifact governance; no code changes before required artifacts exist.

## Task Decomposition Guidance (decomposable only)
- 1) Draft required artifacts (rfc, schema, templates, policy); no code changes.
- 2) Implement CLI entrypoints and structured logs/events with default-off removability.
- 3) Add unit/integration/regression tests with a fixture task.
- 4) Update handover/changelog entries for the rigor layer.
- Order: 1, then 2, then 3, then 4.

## Prompt Body
### Intent
Implement Terminal-Bench-derived rigor gates (outcome verifiers, spec<->test symmetry, oracle solvability, exploit probe, nondeterminism accounting).

### Constraints
- Spec-first, governance-first. Read-only until spec artifacts exist.
- SCOPE (hard limits)
  - Do NOT add leaderboards, competitive scoring, or "agent harness optimization".
  - Do NOT add LLM-as-judge as an enforcement or gating mechanism (advisory-only is allowed later, but not in this todo).
  - Do NOT change execution behavior beyond adding optional verifiers/audits; everything must be removable and off by default unless explicitly gated.

### Scope
OBJECTIVE
- Add five rigor primitives:
  1) Outcome-driven verification: success determined only by explicit verifiers (end-state checks).
  2) Bidirectional spec<->test alignment: enforce "every verifier maps to spec clause" and "every spec clause has verifier".
  3) Oracle solvability proof: require a human-authored oracle script that passes verifiers.
  4) Adversarial exploit probe: a mode that attempts to pass verifiers via shortcuts; must be logged and flagged (not auto-accepted).
  5) Nondeterminism accounting: explicit declaration + measurement of flakiness/external deps; no silent waivers.

### Inputs
- Existing repo governance and prompt artifacts.
- This prompt file.

### Required Reasoning
- Maintain spec-first, governance-first sequencing; no code changes before required artifacts exist.
- Ensure every primitive is independently disable-able/removable and default-off unless explicitly gated.
- Prevent any tool from mutating governance state or auto-certifying success; LLM judge is never a gate.

### Output Artifacts
REQUIRED ARTIFACTS (create before code changes)
- docs/rfcs/rfc-terminal-bench-rigor.md
  - define the five primitives precisely
  - define terminology: "verifier", "oracle", "exploit probe", "nondeterminism"
  - define default-off behavior + removability guarantees
- schemas/rigor.schema.json (or yaml equivalent if repo standard)
  - rigor block schema: verifiers[], spec_map[], oracle{}, exploit_probe{}, nondeterminism{}
- templates/rigor/
  - verifier template (executable + expected outputs)
  - oracle template (human-authored script contract)
  - nondeterminism manifest template (deps, pinning, flaky axes)
- docs/policies/no-llm-judge-gating.md (one-page hard policy)

IMPLEMENTATION TASKS (after artifacts)
- Add CLI entrypoints (or existing CLI integration) for:
  - `rigor verify` (runs verifiers; produces structured report)
  - `rigor check-spec-map` (fails if unmapped spec/test)
  - `rigor run-oracle` (proves solvability; records outputs)
  - `rigor exploit-probe` (runs adversarial probe; always flags results)
  - `rigor nondeterminism report` (records flake metrics + deps)
- Add structured logs/events for every run (append-only).
- Ensure each primitive is independently disable-able and removable.
- Ensure no tool can mutate governance state or auto-certify success.

TESTING REQUIREMENTS
- Add unit tests for schema validation and mapping rules.
- Add integration tests with a tiny fixture task:
  - passing verifier
  - failing verifier
  - missing spec mapping (must fail)
  - oracle passes (must pass)
  - exploit probe "cheat" attempt is detected/flagged (must not auto-pass)
  - nondeterminism manifest required for tasks marked "networked"
- Add regression test ensuring "LLM judge" cannot be enabled as a gate.

DELIVERABLES
- PR with docs + schema + templates + CLI + tests
- Update handover/changelog entries describing the new rigor layer

### Validation Criteria
ACCEPTANCE CRITERIA
- Verifier run produces deterministic pass/fail and a machine-readable report.
- Spec<->test symmetry enforcement is real (fails builds when broken).
- Oracle run demonstrably passes same verifiers and is required for "verified" status.
- Exploit probe can never promote a task to "verified"; only flags risks.
- Nondeterminism reporting exists and prevents silent flaky waivers.
- All components are removable with no impact on core execution paths.

## Validation Criteria
- All ACCEPTANCE CRITERIA in the prompt body are satisfied.
- Required artifacts, CLI integration, tests, and policy updates are complete and comply with constraints.

# RFC: Terminal-Bench Rigor Gates

## Summary
Define a Terminal-Bench-derived rigor layer for CERES that adds outcome verifiers, spec-test symmetry, oracle solvability, exploit probing, and nondeterminism accounting. This layer is optional, default-off, and removable.

## Motivation
CERES needs deterministic, auditable rigor primitives that validate outcomes without relying on model judgment. These gates enforce spec-test alignment, prevent shortcut exploitation, and make nondeterminism explicit without changing default execution behavior.

## Definitions
- Verifier: An explicit, executable end-state check that deterministically returns pass/fail.
- Oracle: A human-authored script that solves the task and must pass the same verifiers.
- Exploit probe: An adversarial run that attempts to pass verifiers via shortcuts; results are always flagged, never accepted.
- Nondeterminism: Any declared external dependency or flaky axis that can affect reproducibility.

## Rigor Primitives
1) Outcome-driven verification
   - Success is determined only by verifier outcomes, not by narrative claims.
2) Bidirectional spec-test alignment
   - Every verifier maps to a spec clause, and every spec clause has a verifier.
3) Oracle solvability proof
   - A human-authored oracle script must pass verifiers to prove solvability.
4) Adversarial exploit probe
   - Runs an adversarial probe; results are logged and flagged, never promoted to verified.
5) Nondeterminism accounting
   - Declare and measure flakiness/external dependencies; no silent waivers.

## Default-Off and Removability
- All rigor primitives are disabled by default.
- Enabling any primitive requires explicit opt-in in governance artifacts.
- Removing this layer must not change core execution paths or outcomes.

## Governance Constraints
- No leaderboards, competitive scoring, or harness optimization.
- No LLM-as-judge as a gate (advisory-only later is allowed, but not here).
- No execution behavior changes beyond optional verifiers/audits.

## Required Artifacts
- docs/rfcs/rfc-terminal-bench-rigor.md (this file)
- schemas/rigor.schema.json
- templates/rigor/ (verifier, oracle, nondeterminism manifest)
- docs/policies/no-llm-judge-gating.md

## Non-Goals
- Any model training or parameter updates.
- Implicit gate escalation or autonomy.
- Runtime behavior changes without explicit opt-in.

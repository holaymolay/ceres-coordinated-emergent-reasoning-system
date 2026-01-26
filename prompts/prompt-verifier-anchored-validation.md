# Prompt: Verifier-Anchored Validation Doctrine

Prompt ID: c0c7c8a9-3ca8-483e-9580-18324d472ed9
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-26T07:22:29Z
Last-Modified: 2026-01-26T16:19:23Z

## Intent
Add verifier-anchored validation doctrine and a minimal enforcement hook so external verification outranks model judgment.

## Constraints
- No new autonomy, no memory features, no self-directed goal generation.
- No new phases unless already present; prefer adding a rule within existing validation/gating.
- Keep changes small and localized; avoid refactors.
- Add/update tests if a gate/lint rule is introduced.
- All changes must be removable without breaking unrelated paths.
- Do not implement any self-improvement, self-generated curriculum, or persistent memory.
- Enforcement must be advisory-only by default; hard gating only when explicitly enabled via an existing policy/config toggle.
- Do not retroactively fail existing artifacts; apply only to newly tagged "verifiable" claims or when explicitly enabled.

## Task Decomposition Guidance (decomposable only)
N/A

## Prompt Body
### Intent
Add a new core principle: "Verifier-Anchored Validation: If something can be verified externally, verification outranks model judgment."

### Constraints
- No new autonomy, no memory features, no self-directed goal generation.
- No new phases unless already present; prefer adding a rule within existing validation/gating.
- Keep changes small and localized; avoid refactors.
- Add/update tests if a gate/lint rule is introduced.
- All changes must be removable without breaking unrelated paths.
- Do not implement any self-improvement, self-generated curriculum, or persistent memory.
- Enforcement must be advisory-only by default; hard gating only when explicitly enabled via an existing policy/config toggle.
- Do not retroactively fail existing artifacts; apply only to newly tagged "verifiable" claims or when explicitly enabled.

### Scope
Task
1) Locate CERES "source of truth" docs for governance/constitution/principles and the execution/validation flow docs.
   - Add a short principle section with:
     - Definition
     - Scope: "only when reliable verifiers exist"
     - Examples: code execution, schema validation, invariant checks
     - Non-goals: not adding learning/memory/drift management
2) Add a lightweight enforcement hook (choose the smallest existing mechanism already used in the repo):
   - Option A: A validator/lint rule that flags outputs/steps labeled "verifiable" unless a verifier result artifact is attached.
   - Option B: A gate in the existing "Check/Validation" step that fails when verifiable claims lack verifier evidence.
   Pick ONE option based on existing repo patterns. Do not create a new framework.
   Default to warning-only unless an existing policy/config toggle explicitly enables hard gating.
3) Add a minimal artifact format for verifier evidence if needed (only if no equivalent exists):
   - Example: artifacts/verifier-evidence.json with fields:
     - spec_id
     - claim_id (or step_id)
     - verifier_type (exec/schema/invariant)
     - verifier_input_ref
     - verifier_output_ref
     - pass_fail
     - timestamp
   Use an existing artifacts directory/pattern if present.
4) Update any relevant templates so future specs/plans can mark steps/claims as "verifiable" and attach evidence references.
5) Add tests:
   - If you added a lint/gate, add unit tests demonstrating:
     - Pass when evidence is present
     - Fail when evidence is missing
   Use existing test tooling and conventions.

Deliverables
- A concise list of files changed with 1-2 lines per file summarizing changes.
- The exact rule text inserted into governance docs.
- Test commands to run and expected pass results.

### Inputs
- Governance/constitution/principles docs.
- Execution/validation flow docs.
- Existing validation/gating mechanisms.

### Required Reasoning
- Choose the smallest existing enforcement mechanism; do not create a new framework.
- Use existing artifact patterns if verifier evidence artifacts are needed.

### Output Artifacts
- Updated governance principle section with the verifier-anchored rule text.
- Enforcement hook implemented via the chosen existing mechanism.
- Optional verifier evidence artifact format only if no equivalent exists.
- Tests for pass/fail evidence conditions when a gate/lint is added.

### Validation Criteria
- Verifiable claims require verifier evidence, or the gate/lint fails deterministically.
- Tests pass for evidence present and missing cases.
- Changes remain localized and removable.
- Default behavior is unchanged unless a policy/config toggle enables hard gating.

## Validation Criteria
- All deliverables and validation criteria in the prompt body are satisfied.

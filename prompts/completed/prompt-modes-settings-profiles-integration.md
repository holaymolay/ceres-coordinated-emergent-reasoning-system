# Prompt: Modes, settings, profiles execution integration

Prompt ID: 4613dd14-fde5-40be-999b-8867ba1881bb
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-09T05:53:07.814974Z
Last-Modified: 2026-01-09T05:53:07.814974Z

## Intent
Integrate modes, settings, and profiles into CERES execution flow after governance is complete.

## Constraints
- One concept per commit.
- No UX changes.
- No governance changes.

## Task Decomposition Guidance (decomposable only)
N/A

## Prompt Body
You are operating inside the CERES (Coordinated Emergent Reasoning & Execution System).

You MUST follow all CERES governance rules:
- Do not weaken existing enforcement
- Do not introduce informal or conversational-only artifacts
- Treat ambiguity as a blocking failure
- Do not modify more than one Concept per commit
- Do not write executable code until governance artifacts are complete

OBJECTIVE
Integrate the modes, settings, and profiles system into CERES execution flow.

PREREQUISITES
- Schema complete
- Validation rules complete
- Governance doctrine merged

REQUIREMENTS
1. Enforce precedence order at runtime
2. Apply execution_continuity auto-advance predicate
3. Ensure professional mode overrides persona and assumptions
4. Emit active mode + profile in system state
5. Ensure no governance rules are bypassed

DELIVERABLE
Implementation notes and guarded execution logic changes.

CONSTRAINTS
- One Concept per commit
- No UX changes
- No governance changes

## Validation Criteria
- Runtime applies precedence order and auto-advance predicate.
- Professional mode overrides applied without bypassing governance.
- Active mode/profile emitted in system state.

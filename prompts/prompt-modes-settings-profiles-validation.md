# Prompt: Modes, settings, profiles validation rules

Prompt ID: 30e6f1a4-8eb6-47bb-ae86-17132871e229
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-09T05:53:07.814974Z
Last-Modified: 2026-01-09T05:53:07.814974Z

## Intent
Define machine-checkable validation rules for modes, settings, and execution profiles.

## Constraints
- No execution code or UX.
- No governance prose.

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
Define formal validation rules for the modes, settings, and execution profiles schema.

INPUTS
- The previously defined schema

REQUIREMENTS
1. Define illegal combinations, including:
   - professional mode + assumption-permitting settings
   - profile overrides that escalate beyond base mode permissions
2. Define auto-downgrade rules:
   - professional mode defaults execution_continuity to manual
3. Define required confirmations when relaxing control discipline
4. Define the auto-advance predicate for execution_continuity = auto-safe
5. Validation rules must be machine-checkable

DELIVERABLE
A validation rules document or schema extension that can be enforced programmatically.

CONSTRAINTS
- No execution code
- No UX
- No governance prose

## Validation Criteria
- Rules cover illegal combinations, auto-downgrades, confirmations, and auto-advance predicate.
- Validation output is machine-checkable and enforcement-ready.

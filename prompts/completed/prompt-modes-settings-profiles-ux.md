# Prompt: Modes, settings, profiles interaction flow

Prompt ID: fce66c82-f265-4540-9678-35cfb3c9153f
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-09T05:53:07.814974Z
Last-Modified: 2026-01-09T05:53:07.814974Z

## Intent
Design the CLI/chat interaction flow for managing settings and execution profiles.

## Constraints
- No execution logic.
- No state mutation described.
- Rendering layer only.

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
Design the CLI / chat interaction flow for managing CERES settings and execution profiles.

INPUTS
- Schema
- Validation rules
- Governance doctrine

REQUIREMENTS
1. `/settings` entry point
2. Menu-based navigation
3. Profiles submenu:
   - list
   - activate
   - save current as profile
   - update profile
   - delete profile
4. Explicit confirmation prompts when control discipline is relaxed
5. Clear display of:
   - active mode
   - active profile

DELIVERABLE
A text-based interaction flow specification.

CONSTRAINTS
- No execution logic
- No state mutation described
- This is a rendering layer only

## Validation Criteria
- Flow includes /settings entry point, menus, profile actions, confirmations, and status display.

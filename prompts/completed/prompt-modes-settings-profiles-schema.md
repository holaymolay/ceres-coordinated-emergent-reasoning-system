# Prompt: Modes, settings, profiles schema

Prompt ID: c64a26b5-99cf-490f-814d-86d41c06e46b
Classification: atomic
Status: draft
Owner: user
Created: 2026-01-09T05:53:07.814974Z
Last-Modified: 2026-01-09T05:53:07.814974Z

## Intent
Define the formal schema for CERES interaction modes, settings, and execution profiles.

## Constraints
- Schema only; no execution logic or UX.
- No governance prose yet; governance excluded from schema.

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
Define a formal, machine-readable schema for CERES interaction modes, execution settings, and user-defined execution profiles.

SCOPE
- Schema only
- No execution logic
- No UX
- No governance prose yet

REQUIREMENTS
1. Define Interaction Modes:
   - guided
   - standard
   - professional
2. Define configurable settings including:
   - execution_continuity (manual | auto-safe | continuous)
   - autonomy_level
   - questioning_policy
   - output_density
   - failure_handling
   - progress_signaling
   - safety_level
3. Define Execution Profiles:
   - named
   - reference a base interaction mode
   - store only overrides (diffs)
4. Define precedence order:
   system_defaults → mode_defaults → profile_overrides → session_overrides
5. Governance must be explicitly excluded from the schema
6. Schema must support validation (illegal combinations detectable)

DELIVERABLE
Produce a versioned YAML schema file suitable for long-term use in CERES.

CONSTRAINTS
- No prose explanations
- No examples outside schema comments
- Schema must be strict and explicit

## Validation Criteria
- Schema defines modes, settings, profiles, and precedence order.
- Governance is excluded from schema scope.
- Schema is strict and validation-ready.

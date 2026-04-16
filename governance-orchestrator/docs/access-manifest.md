# Access Manifest (Policy)

This document defines the default access posture for repository automation and Skills. It is used by the Security/Gatekeeper roles as a review checklist against declared access in `skill.yaml`.

## Default Policy
- Network: denied
- Subprocess: denied
- Filesystem writes: denied (prefer stdout-only Skills)
- Environment variables: denied unless explicitly allowlisted

## How Skills Declare Access
Each Skill must declare access under `skill.yaml:security.access`:
- `filesystem.read`: repo-relative globs the Skill may read
- `filesystem.write`: repo-relative globs the Skill may write
- `env.read`: explicit env var names the Skill may read
- `subprocess.allowed`: boolean
- `network.allowed`: boolean

## Review Checklist (Security Agent)
- Validate `skill.yaml` against `skills/_schema/skill.schema.json`.
- Confirm requested access is minimal and consistent with `determinism.*`.
- If `network.allowed=true`:
  - Require an explicit approval reference (e.g., `x-securityApprovalId`).
  - Require a documented connector boundary (no ad-hoc outbound calls).
- If filesystem writes are requested:
  - Prefer writes under an explicit output directory (stack-appropriate) and keep artifacts out of VCS.

## Exceptions
Exceptions must be explicitly documented and approved. Record the approval reference in the Skill (`x-securityApprovalId`) and summarize it in `handover.md`.

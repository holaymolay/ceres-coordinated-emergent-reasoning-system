# Self-Audit Protocol (Governance)
Status: Governance definition for CERES Self-Audit. Non-automated; human/agent co-signed ritual.

## Purpose
- Periodically verify governance integrity, artifact discipline, and invariants.
- Surface drift or violations early via documented findings.
- Provide evidence for Signals and future audits; never auto-fix.

## Cadence
- At least quarterly or after major governance/runtime changes.
- Additional ad-hoc audits allowed when triggered by Signals or doctor findings.

## Authority
- Non-executable; audits do not alter governance on their own.
- Findings are informational; any remediation requires standard governance/change control.
- Auto-certification by LLMs is explicitly forbidden.

## Scope
- Workspace artifacts: todo/plan, gap/objective artifacts, memory/handover, prompts.
- Governance integrity: CONSTITUTION, AGENTS, enforcement scripts/hooks present and pinned.
- Observability: events/logs capture, Signals/doctor outputs.
- Nested layout: .ceres/core pinning and workspace presence.

## Required Inputs
- Latest doctor report (text or JSON).
- Relevant Signals since last audit.
- Current artifacts (todo.md, gap-ledger.json, objective-contract.json, memory, handover).
- Core lock state (core.lock).

## Outputs
- Completed self-audit artifact (templates/self-audit.md) stored under version control.
- Explicit findings, violations (or “none”), actions (or “none”), signatures.

## Prohibitions
- No auto-remediation, no scheduling changes, no mode/profile changes.
- No silent updates to governance documents.
- No delegation of sign-off to automated agents; human or designated reviewer must sign.

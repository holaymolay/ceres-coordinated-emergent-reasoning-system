# Security Playbook

This repository defines governance for agent-assisted software delivery. This document codifies the minimum security posture for specs, Skills, Concepts, Synchronizations, and operational artifacts.

## Core Rules
- Never commit real secrets (API keys, tokens, private keys, customer data).
- Default-deny outbound network access for Skills and automation.
- Enforce least privilege: declare and review access before execution.
- Prefer deterministic, offline workflows; treat nondeterminism as a security risk.

## Secrets & Sensitive Data
- Use `.env.sample` (or stack-equivalent) to document required environment variables with safe defaults.
- Do not log secrets or PII. Redact before writing logs or fixtures.
- If a secret is committed:
  1) Revoke/rotate immediately.
  2) Remove from git history if required by policy.
  3) Document the incident, remediation, and prevention steps in `handover.md`.

## Skill Security (Deterministic Tooling)
- Skills must declare access under `skill.yaml:security.access` and follow the Access Manifest (`docs/access-manifest.md`).
- Network access is forbidden unless explicitly declared and approved.
- Subprocess execution is forbidden unless explicitly declared and approved.
- Filesystem writes are forbidden unless explicitly declared; prefer stdout-only Skills.

## Dependency Hygiene
- Use stack-specific audit tools (see `docs/stacks/`) where applicable.
- Pin dependencies in a lockfile when the stack supports it.
- Avoid vendoring third-party libraries unless necessary and documented.

## Incident Response (Minimum)
- Contain: revoke credentials, disable compromised integrations, pause automated runs if uncertain.
- Assess: identify affected data/systems and the source of exposure.
- Remediate: patch root cause, add regression checks (lint/tests/scans).
- Communicate: update `handover.md` and create a follow-up todo (via `todo-inbox.md`) if ongoing work is required.

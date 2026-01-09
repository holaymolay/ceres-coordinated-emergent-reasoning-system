# Todo (CERES template)

## Bugs
- [ ] 

## Workflow Governance
- [ ] 

## Current Focus
- [ ]


## Next Features & Updates
- [x] TODO 1.1 — Define Signals governance (docs/signals.md; informational-only, authority/prohibitions/inputs/outputs; reference constitution).
- [x] TODO 1.2 — Define initial Signals catalog (docs/signals-catalog.yaml; 5–7 signals with severity/source/constitutional_reference/message; no recommendations).
- [x] TODO 1.3 — Implement minimal Signals emitter (read-only; CLI notices + append-only .ceres/workspace/events.jsonl; no scheduling/enforcement; fail closed if workspace missing).
- [x] TODO 2.1 — Formalize Doctor scope (docs/doctor.md; non-authoritative, project-scoped, feeds Signals/Self-Audit; enumerate forbidden checks).
- [x] TODO 2.2 — Implement doctor CLI (.ceres/bin/doctor; workspace detection, core.lock integrity, wrapper parity, feature flags, removal-proof invariants; human + optional JSON; no fixes).
- [x] TODO 2.3 — Wire doctor findings to Signals (one-way translation; doctor remains evidence-only).
- [x] TODO 3.1 — Define Self-Audit protocol (docs/self-audit.md; cadence/scope/authority/inputs/outputs; ban auto-certification).
- [x] TODO 3.2 — Create Self-Audit template (templates/self-audit.md; context/evidence/findings/violations/actions/sign-off).
- [x] TODO 3.3 — Implement audit reminder signal (Signals checks last audit timestamp; emits self_audit_overdue notice; never triggers audit or blocks execution).


## Backlog
- [ ] Minimize CERES footprint in new projects (smallest visible files/folders without losing required artifacts).
- [ ]

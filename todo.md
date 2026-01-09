# Todo (CERES template)

## Bugs
- [ ] 

## Workflow Governance
- [ ] 

## Current Focus
- [ ]


## Next Features & Updates

- [ ] Execute prompt: prompts/prompt-modes-settings-profiles-governance.md
      Outcome: Codify modes/settings/profiles governance rules.
- [ ] Execute prompt: prompts/prompt-modes-settings-profiles-ux.md
      Outcome: Specify settings/profiles interaction flow.
- [ ] Execute prompt: prompts/prompt-modes-settings-profiles-integration.md
      Outcome: Integrate modes/settings/profiles into execution flow.

- [ ] Define recursive, environment-mediated execution mode (non-user-visible; disabled by default; no LLM escalation; default unchanged).
- [ ] Harden recursive execution governance language (MUST/MUST NOT, close loopholes, verify backward compatibility; block on ambiguity). (depends on: recursive execution mode declared)
- [ ] Define non-authoritative execution-pressure signals (no authority, no intent, explicit emit/do-not-emit rules). (depends on: governance hardening)
- [ ] Define arbitration-only escalation rules (approval/denial conditions, hard ceilings, required observability). (depends on: governance hardening + signals)
- [ ] Implement execution adapter after arbitration approval (artifact-only recursion, budgeted termination, locked finalization; no change without approval). (depends on: arbitration rules)
- [ ] Measure recursive execution impact and decide promote/retain/remove (baseline vs escalated, failures, costs, wins, regressions). (depends on: execution adapter)

## Backlog
- [ ] Minimize CERES footprint in new projects (smallest visible files/folders without losing required artifacts).
- [ ]

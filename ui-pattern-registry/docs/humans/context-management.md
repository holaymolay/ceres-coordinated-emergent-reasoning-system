# Context management rationale

This document explains, in a falsifiable way, how the framework reduces effective context pressure and makes long-running AI workflows resumable.

## Context control through externalized state (why it works)

### Problem statement
- Drift: conversational reminders decay and rules diverge from intent.
- Re-derivation: the model re-explains requirements instead of executing them.
- Token bloat: repeated restatement of constraints consumes budget without adding signal.
- Implicit rule loss: unpinned agreements vanish when the chat window truncates.

### Architectural shift
- Memory is externalized into versioned artifacts (`specs/`, `todo.md`, `handover.md`, `runs/`).
- Narrative context is replaced by symbolic references (spec IDs, Concept manifests, Synchronizations).
- Control-plane chat is separated from the state-plane repo; `AGENTS.md` defines authority and boundaries.

### Mechanisms (referential and enforced)
- `AGENTS.md` forces spec-first execution and bans free-form prompting; specs live in `specs/`.
- Concepts and manifests (`concepts/`) scope handlers; Synchronization manifests (`synchronizations/`) declare cross-concept dependencies explicitly.
- PDCA and CI (`docs/agents.md`, `.github/workflows/`) enforce lint, schema, and governance gates on every change.
- Handover + run records (`handover.md`, `runs/`) rehydrate state without replaying prior chat.
- README governance (`README_GOVERNANCE.md`, `README_SPEC.yaml`) prevents entrypoint drift.

### Why this reduces effective context pressure
- The model no longer “remembers” rules; it reloads specs, manifests, and ledgers as inputs.
- Rehydration pulls artifacts (handover, todo, spec IDs) so truncation does not erase constraints.
- Lost chat tokens do not remove rules because CI and validators reject out-of-contract outputs.

### Practical consequences
- Longer productive sessions with stable constraints.
- Fewer correction loops because constraints are re-read instead of re-taught.
- Easier restarts: load `handover.md`, `todo.md`, and relevant specs to continue.
- Lower cognitive load for humans: follow the documented map instead of restating context.

### Non-claims / boundaries
- Does not increase raw token limits.
- Does not guarantee correctness without maintained specs and passing CI.
- Requires disciplined updates to specs, manifests, and handover artifacts.

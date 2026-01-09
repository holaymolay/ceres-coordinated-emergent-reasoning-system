# Non-Authoritative Execution-Pressure Signals

## Purpose
Provide advisory-only signals when execution difficulty is detected, without altering execution authority or flow.

## Signal Properties
- Non-binding; cannot change mode, routing, or execution behavior.
- Emitted by planners/executors as telemetry only.
- Must include: task_id, spec_id (if available), reason, evidence, suggested next_step (textual).
- Routed to observability; arbitration may review but signals carry zero authority.

## When Emitted (Allowed)
- Repeated retries on the same task with no progress.
- Dependency blockage outside current task scope.
- Tooling/environment unavailability that blocks progress.
- Detected ambiguity not resolvable within current task boundaries.

## When Not Emitted (Forbidden)
- To request recursion or escalation directly.
- To bypass governance gates or preflight outcomes.
- On first failure without evidence of systemic blockage.

## Required Handling
- Emit as structured event (`execution_pressure_signal`) with reason + evidence summary.
- Must not pause or alter execution; continue under current governance.
- Arbitration reviews signals; only Arbitration may approve escalation.

## Compatibility
- Coexists with modes/settings/profiles; does not override professional-mode constraints.
- No changes to execution continuity; signals are advisory telemetry only.

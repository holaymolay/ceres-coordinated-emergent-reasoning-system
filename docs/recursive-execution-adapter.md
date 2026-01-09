# Recursive Execution Adapter (Post-Arbitration)

## Purpose
Provide a guarded adapter for environment-mediated recursion only after explicit Arbitration approval.

## Activation
- Triggered only when Arbitration emits an approved `execution_escalation_decision` for the current task/spec.
- Default path remains unchanged; adapter is dormant without approval.

## Behavior (when approved)
- Enforce artifact-only recursion: each recursive step must be tied to a task/artifact update; no free-form execution.
- Enforce budgeted termination: must honor declared depth/time/cost budget from Arbitration; abort on exceed.
- Lock finalization: results must be written back to governed artifacts; exit returns to standard execution.
- Maintain PDCA: preflight, lifecycle, observability, and security remain mandatory for each recursive step.

## Forbidden
- Bypassing preflight, observability, or security checks.
- Altering Task Plan without governance update.
- Nested recursion beyond approved depth.
- Changing execution_continuity or safety_level outside approved settings.

## Observability
- Emit events for entry (`recursive_adapter_enter`), step (`recursive_adapter_step`), and exit (`recursive_adapter_exit`) with: spec_id, task_id, run_id, budget usage (depth/time), and status.
- Emit failure events on budget/violation (`recursive_adapter_fail`).

## Fallback
- On violation or budget exceed, abort recursion and return control to standard execution; record failure event.

## Integration Notes
- Adapter is an execution-layer component; governance/arbitration remain authoritative.
- No UX changes; adapter is invoked by the runtime when an approved escalation token is present.

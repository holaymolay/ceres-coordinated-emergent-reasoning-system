# Arbitration Rules for Recursive, Environment-Mediated Execution

## Approval Conditions (all required)
- Active spec_id with ready-for-planning artifacts and approved Task Plan
- No blocking gaps; no open ClarificationRequests
- Observability and security hooks active and writable
- Termination/budget declared (depth/time/cost); continuous recursion prohibited
- Execution-pressure signal(s) present with evidence

## Denial Conditions (any triggers denial)
- Missing or invalid spec_id / Task Plan / observability hooks
- safety_level = maximal
- execution_continuity = continuous in any active setting
- Attempted LLM/user-initiated escalation request
- Unbounded or undefined recursion budget

## Hard Ceilings
- Single escalation per task unless explicitly re-approved
- Max recursion depth = 1 (no nested recursion beyond one level)
- Max recursion duration must be declared and enforced externally

## Observability Requirements
- Emit `execution_escalation_decision` with: decision (approved/denied), reason, spec_id, task_id, budget, requester (Arbitration), run_id
- Log all entry/exit points; nonconformant logs are violations

## Enforcement Notes
- Arbitration is the sole authority to approve or deny recursion; planners/executors cannot bypass
- Approval does not relax governance, PDCA, or security; all existing gates remain active
- Denial must halt escalation and continue in standard execution mode

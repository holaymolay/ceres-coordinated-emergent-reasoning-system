# Context Management & Inter-Agent Protocol

This document operationalizes the context-segmentation workflow introduced in `AGENTS.md`. It defines ledger locations, the pruning lifecycle, inter-agent messaging, and archival requirements so every Codex agent shares only what is necessary while maintaining a full audit trail.

## 1. Ledger Layout

| Agent | Ledger Path | Primary Contents |
|-------|-------------|------------------|
| Coordinator | `docs/context/coordinator.md` | Intake triage, Concept ownership map, escalation notes |
| Router | `docs/context/router.md` | Routing heuristics, Skill lookup cache, pending inbox entries |
| Planner / Task Manager | `docs/context/planner-task-manager.md` | Active plans, domain-shift markers, open subtasks |
| Caching Agent | `docs/context/caching-agent.md` | Cache keys, eviction schedule, hit/miss stats |
| Arbitration Agent | `docs/context/arbitration-agent.md` | Priority queue snapshots, conflict resolutions |
| Observability Agent | `docs/context/observability-agent.md` | Metrics thresholds, alert statuses |
| Pruning Agent | `docs/context/pruning-agent.md` | Open prune tickets, approvals, archive registry |
| Security Agent | `docs/context/security-agent.md` | Credential scopes, approval references, incident notes |

Additional agents inherit the same pattern: create `docs/context/<agent>.md` and record only the data that agent is authorized to see.

Each ledger entry uses the following structure:

```
## <Date ISO8601> — <Concept/Feature>
- Summary: <one-line>
- Details: <bullet list as needed>
- Related Spec / Skill: <ID or n/a>
- Pending Actions: <owner + due date>
```

## 2. Domain Shift Detection

The Planner stamps a domain-shift entry whenever:
- The active todo references a different Concept than the previous task.
- A user explicitly asks to switch focus (even within the same Concept but with unrelated functionality).
- Context size exceeds two screens of text in any ledger.

Domain-shift entries ping the Pruning Agent automatically so stale context can be reviewed.

## 2.1 Daily Usage Checklist

1. **Open ledger entry:** Before starting a task, append an entry to the owning agent’s ledger noting the todo/spec being executed and today’s date.
2. **Update during work:** When the plan advances (new subtasks, discoveries, blockers), append bullet updates beneath the same entry so reviewers see the evolution.
3. **Reference IDs:** Include the ledger entry heading (date + Concept) when writing `completed.md`, `CHANGELOG.md`, or `handover.md` updates so the audit trail links together.
4. **Close out:** Once the task completes, mark the entry with a short outcome line (`Status: completed`, `Status: blocked`, etc.) before triggering any pruning.

## 3. Pruning Checklist

1. **Identify candidate entries** — filter ledger sections older than two completed tasks or unrelated to the new domain.
2. **Draft prune summary** — capture agent, Concept, entry count, and rationale.
3. **Request approval** — message the user/owner with the summary and await explicit confirmation.
4. **Archive** — move the entries into `docs/context/archive/<timestamp>-<agent>.md`. Include the original headings and any linked specs.
5. **Back-reference** — in the live ledger, add `> Pruned on <date> → archive/<file>` so auditors can trace history.
6. **Log the action** — update `completed.md` and `handover.md` with the prune reference and reasoning.

If approval is denied, annotate the ledger entry with `Prune Deferred — reason`.

## 4. Inter-Agent Requests

All context sharing goes through ledger-based messages:

```
### Context Request — <Requester> → <Owner>
- Concept / Spec: <identifier>
- Need: <concise summary>
- Deadline: <timestamp or ASAP>
```

The owner responds inline with:

```
> Response (<Granted|Declined>) — <Owner> — <timestamp>
> Notes: <excerpt or decline reason>
```

The Pruning Agent monitors outstanding requests via `docs/context/pruning-agent.md` to ensure follow-through and to purge stale communication chains during pruning.

## 5. User Interaction Hooks

- Pruning cannot proceed without the user’s approval. Record approvals in the pruning-agent ledger and quote them when archiving.
- When approvals are slow, add a reminder entry rather than pruning unilaterally.
- During large clean-ups, batch entries by Concept so the user can approve per-feature rather than per-note.
- Clarification checkpoints: If a user requests the same fix more than twice, pause implementation, restate your understanding in the ledger or plan entry, log the user’s clarification, and only resume after alignment. This keeps the audit trail clear and prevents churn.

## 6. Efficiency Practices

- Prefer links to specs, issues, or commits instead of copying long excerpts.
- When a new Concept engagement begins, start with a clean ledger section so context remains concise.
- Use the archive folder to store historical context; never delete without archival.

Following this process keeps every agent’s context lightweight, auditable, and ready for rapid domain shifts without sacrificing institutional memory.

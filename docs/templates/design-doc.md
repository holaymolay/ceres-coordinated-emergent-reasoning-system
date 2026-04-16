# Design doc: <title>
This design doc captures a scoped technical decision and its rationale.
Use it to communicate the chosen path and the reasons behind it.
Keep the document short so readers can scan it quickly.
Link to supporting material only when it changes the decision.

## Problem
Describe the user or system problem in concrete terms.
Focus on outcomes and constraints rather than implementation details.
Keep the scope limited to the decision at hand.

- Who is affected and how.
- What breaks or slows down without a change.
- What success looks like in one sentence.

## Constraints
List the non-negotiable limits that shape the decision.
Keep each constraint short and testable.

- Constraint tied to time, cost, or compliance.
- Constraint tied to platform or dependencies.
- Constraint tied to operational support.

> WARNING: Include only constraints that materially limit options.

## Decision
```text
Decision: <short, single-sentence decision statement>
```
Use the line above to capture the final choice in one sentence.
Add only the minimum detail needed to interpret it.

## Tradeoffs
Explain what improves and what degrades with this decision.
Use a comparison table only when it clarifies the tradeoffs.

| Option | Benefit | Cost |
| --- | --- | --- |
| Option A | Primary upside | Primary downside |
| Option B | Secondary upside | Secondary downside |

## Non-goals
Clarify what this decision does not attempt to solve.

- Out-of-scope behavior or feature.
- Deferred improvement or refactor.
- Work handled by another system.

## Rationale
State the reasoning that led to the decision.
Keep it factual and focused on the constraints and tradeoffs.

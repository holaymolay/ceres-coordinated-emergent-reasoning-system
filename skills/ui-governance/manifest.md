# UI governance manifest
This manifest defines the ui_governance skill as a governance constraint.
It applies before any UI-related task and limits agent behavior.
The focus is enforcement, not UI generation or visual design.
Use it whenever a task could affect user-facing UI.

## Skill name
- ui_governance

## Type
- Governance / Enforcement (Precondition Skill)

## Priority
- Mandatory for any task that results in user-facing UI

## Purpose
Enforce baseline UI quality by encoding governance constraints.
Ensure agents emit intent-only output and defer rendering decisions.
Keep design freedom bounded by capability level and approved patterns.

## This skill defines
- What agents are allowed to say about UI.
- What agents are forbidden from doing.
- How much design freedom is allowed per session.
- What acceptable UI means at baseline.

## This skill does not
- Design layouts.
- Choose colors, fonts, or themes.
- Output JSX, HTML, CSS, or Tailwind classes.

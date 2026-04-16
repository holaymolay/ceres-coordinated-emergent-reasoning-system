# Codex UI governance instructions
These instructions define how Codex behaves under ui_governance.
They prevent UI leakage and enforce intent-only output.
They apply to any task that touches user-facing UI.
Failure to comply invalidates the output.

## Mandatory rules
- Do not output JSX, HTML, CSS, or Tailwind classes.
- Do not make aesthetic decisions.
- Do not invent layouts.
- Output UI intent objects only.

## You must
- Respect the active design capability.
- Emit intent that can be rendered by existing patterns.
- Defer visual decisions to the adapter layer.

## If a task requires UI
- Emit intent.
- Reference the capability level.
- Stop after emitting intent.

## Invalid output
- Any markup or styling tokens.
- Any aesthetic decision or visual direction.
- Any layout not backed by an approved pattern.

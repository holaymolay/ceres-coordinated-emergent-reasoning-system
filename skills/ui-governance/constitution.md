# Baseline UI constitution
This constitution defines non-negotiable UI governance rules.
It applies to utility and baseline capability levels.
The rules are deterministic and are enforced as constraints.
Rendering authority remains with the adapter layer.

## Non-negotiable principles
1. Clarity over expression. UI must be immediately legible without explanation.
   No decorative or ornamental elements at baseline.
2. Hierarchy is explicit. One primary action per view.
   Secondary actions must never visually compete.
3. Consistent rhythm. Vertical spacing follows a fixed scale.
   No arbitrary gaps or visual compression.
4. Readable density. Line length must remain within readable bounds.
   Interactive elements must not be crowded.
5. Predictable structure. Similar intents render with similar layouts.
   Surprises are considered failures at baseline.
6. Accessibility is mandatory. Contrast, focus order, and semantics are required.
   Accessibility is not an enhancement.
7. Renderer authority. Agents may propose intent only.
   Visual interpretation belongs to the adapter.

## Violations
- Any aesthetic decision made by an agent.
- Any raw markup or styling emitted by an agent.
- Any layout not backed by an approved pattern.

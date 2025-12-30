# Ecosystem Map

## Relationships and Call Directions
- `cef-governance-orchestrator` sets governance patterns and may reference tooling from other components but does not own their runtime.
- `cef-readme-spec-engine` is consumed by repos that need deterministic README generation; it does not call other components.
- `cef-spec-compiler` can consume governance rules and visual constraints but does not control those sources.
- `cef-ui-constitution` supplies visual constraints consumed by renderers or compilers; it does not depend on other components.
- `cef-ui-pattern-registry` provides approved UI patterns that downstream renderers or pipelines may import; it does not orchestrate other repos.

## Umbrella Repo Placement
- The umbrella repository is a coordination layer only and is **never** in the runtime execution path of any component.
- Components communicate through published artifacts (specs, schemas, packages), not through this umbrella repo.

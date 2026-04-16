# What Is a Pattern?

A pattern in this registry is a structural composition contract. It declares the role of the pattern, its required and optional parts, how deeply it may nest, and where it is allowed or forbidden.

## Required declarations
- Identity: `pattern_id`, `name`, `category` (`layout`, `composition`, or `interaction`), `version`, and `status`.
- Roles: `roles.required_roles` (semantic roles, not components) plus optional roles.
- Structure: `structure.required_parts`, optional parts, and `max_nesting_depth`.
- Usage constraints: `allowed_page_goals`, `allowed_interaction_density`, `forbidden_intents`, `animation_allowed`.
- Composability: `allowed_child_categories` / `allowed_parent_categories` plus optional allow/forbid lists by `pattern_id`.
- Variants: optional structural variants with clear allow conditions.

## What a pattern is not
- It is **not** a component, markup file, or design token set.
- It is **not** a renderer or adapter; enforcement happens elsewhere.
- It is **not** stylistic guidance; visuals are defined by consuming systems.
- It is **not** agent logic or workflow prompts.

## Schema alignment
All pattern files must validate against `schemas/pattern.schema.json`. The schema enforces field presence, enums, and structural constraints so CI can reject incomplete or non-conforming definitions.

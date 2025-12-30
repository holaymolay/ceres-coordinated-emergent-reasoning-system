# Repository Roles

## cef-governance-orchestrator
- **Role**: Governance and context-engineering framework for coding agents.
- **Responsibilities**: Define agent operating contracts, context ledgers, and governance workflows; host enforcement specs for agent behavior.
- **Non-Responsibilities**: Does not manage product-specific code, UI assets, or downstream release artifacts.

## cef-readme-spec-engine
- **Role**: Deterministic README generator and validator.
- **Responsibilities**: Convert README specs into artifacts; validate structure and tone against declared rules.
- **Non-Responsibilities**: Does not enforce policies in other repos or own their governance; no marketing copywriting.

## cef-spec-compiler
- **Role**: Compiler-style pipeline that turns clarified intent into governed specs.
- **Responsibilities**: Enforce stage gates for intent capture, clarification, normalization, validation, and synthesis.
- **Non-Responsibilities**: Does not generate business logic or UI; does not assume ownership of renderer policies.

## cef-ui-constitution
- **Role**: Machine-readable visual constitution for UI constraints.
- **Responsibilities**: Provide schemas and limits for typography, spacing, color, motion, and related visual domains.
- **Non-Responsibilities**: Does not ship UI components, styling tokens, or renderer implementations.

## cef-ui-pattern-registry
- **Role**: Registry of approved UI patterns for LLM-driven front ends.
- **Responsibilities**: Define pattern schemas and curated pattern library; supply validation tooling for pattern compliance.
- **Non-Responsibilities**: Does not manage branding/styling, component libraries, or orchestration workflows.

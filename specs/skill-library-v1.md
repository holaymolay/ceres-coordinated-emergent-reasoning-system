Spec Title: Skill Library v1 (Deterministic, LLM-agnostic)
Spec ID: 6f34688b-a76e-46b8-8d2d-8ffe5c88f9c6
User Story: As a delivery team, I need a deterministic Skill library that runs without any LLM so that agents can select/parameterize Skills while execution remains testable, portable, and secure.

Functional Requirements:
- Define a canonical Skill package layout under `skills/` that scales to hundreds of Skills and supports isolated testing.
- Define a portable Skill contract (`skill.yaml`) with schema-defined I/O (JSON Schema), explicit determinism constraints, and explicit security/access declarations.
- Provide a deterministic conversion protocol to normalize upstream “skills/tools” into repository-native Skills without embedding prompts or memory.
- Define an upstream ingestion policy for common tool ecosystems (Codex Skills, Anthropic Skills, Semantic Kernel, LangChain tools, MCP servers).
- Define a foundational Skill taxonomy (v1) focused on cross-domain infrastructure capabilities (no project-specific business logic).
- Define mechanical integration points with Concepts, Synchronizations, PDCA logs, Security governance, Observability, and caching.

Non-functional Requirements:
- Deterministic execution: Skills must be stateless and executable without an LLM; outputs must be a pure function of declared inputs and allowed reads.
- Portability: Skills must be callable from Codex/GPT/Claude/MCP/CLI and not require vendor-specific SDKs in the execution path.
- Testability: Every Skill must be runnable and testable offline; tests must not depend on network or wall-clock time.
- Governance: Every Skill must reference a Spec ID; Skill changes are auditable and follow “one Skill per commit” for Skill packages.

Architecture Overview:
- Authoritative design and normative requirements live in `docs/skills/skill-library-v1.md`.
- The Skill system is “capability infrastructure”:
  - LLMs/agents select and parameterize Skills.
  - Skills execute deterministically via declared runtime commands with JSON stdin/stdout.
  - Skills never contain prompts, memory, planning, or interactive questioning logic.

Language & Framework Requirements:
- Skill implementations may be in Python, Node.js, or POSIX shell (or any language callable as a deterministic command), but must be runnable in CI without LLM access.
- Skill contracts and I/O schemas are technology-neutral (YAML + JSON Schema).

Testing Plan:
- Validate every `skill.yaml` against a repository schema (`skills/_schema/skill.schema.json`).
- Validate every Skill’s input/output against the Skill’s declared `schemas/input.schema.json` and `schemas/output.schema.json`.
- Require at least one offline “smoke” test per Skill with fixtures checked into `skills/<slug>/fixtures/`.

Dependencies:
- JSON Schema tooling for validation (language-specific, CI-controlled).
- YAML parsing tooling for `skill.yaml` validation (language-specific, CI-controlled).

Input/Output Schemas:
- Every Skill declares:
  - `schemas/input.schema.json` for inputs.
  - `schemas/output.schema.json` for outputs.
- Skills accept input JSON via stdin and emit output JSON via stdout.

Validation Criteria:
- Repository contains:
  - `docs/skills/skill-library-v1.md` with the v1 design artifacts and locked conversion template.
  - `skills/_template/` providing Skill scaffolding guidance.
  - `skills/_schema/skill.schema.json` to validate `skill.yaml`.
- Skill governance rules are enforceable via schema validation (required Spec ID, determinism flags, access declarations, and extension rules).

Security Constraints:
- No network access by default; any network-enabled Skill requires explicit declaration and Security approval.
- No external calls without approved connectors; secrets must never be embedded in Skill packages.
- All filesystem/env/subprocess access must be declared and reviewed.

# Skill Library Refinement (v1)

This document defines a first-class, LLM-agnostic Skill system for this repository. It refines the existing governance by making Skills deterministic, schema-defined, and executable without any LLM present.

## 1. Executive Summary (≤ 10 bullets)
- Skills are deterministic tool packages: stateless, schema-defined I/O, executable without any LLM.
- LLMs select and parameterize Skills; agents orchestrate; Skills execute (no prompts/memory/planning inside Skills).
- Skill packages live under `skills/<skill-slug>/` with `skill.yaml`, `schemas/`, `impl/`, `tests/`, and `fixtures/`.
- Every Skill references a Spec ID and is testable offline in isolation.
- The Skill contract is portable across Codex/GPT/Claude/MCP/CLI via JSON stdin/stdout and JSON Schema validation.
- Security is enforceable via declared access in `skill.yaml` and a repo Access Manifest; network is forbidden by default.
- Observability is enforceable via a required run report contract and structured logs.
- Ingestion from upstream “skills/tools” is allowed only after normalization into this deterministic contract (no vendor SDK in runtime path).
- “One Skill per commit” applies to Skill packages; shared runtime/schema infrastructure is committed separately.
- Skills are shared infrastructure, not Concept business logic; cross-concept effects require Synchronization contracts.

## 2. Skill Repository Architecture

### 2.1 Canonical Layout
```
skills/
  _schema/
    skill.schema.json
  _template/
    SKILL.template.md
    skill.yaml
    schemas/
      input.schema.json
      output.schema.json
    impl/
      run.sh
    tests/
      test_smoke.sh
  <skill-slug>/
    skill.yaml
    README.md
    schemas/
      input.schema.json
      output.schema.json
    impl/
      run.(py|js|sh)
    tests/
      ...
    fixtures/
      ...
```

### 2.2 Naming Conventions
- `skills/<skill-slug>/` uses `kebab-case` and is stable once published.
- `skill.yaml:id` uses a dot namespace with snake segments: `^[a-z][a-z0-9_]*(\\.[a-z][a-z0-9_]*)*$` (example: `schema.validate_json`).

### 2.3 Versioning Strategy
- Each Skill uses SemVer: `skill.yaml:version: X.Y.Z`.
- Contract evolution is explicit via `apiVersion: skill/v1`.
- Breaking changes require a major version bump and fixture/test updates.

### 2.4 Language Support Policy (TS / Python / Shell)
- Skills may be implemented in any language callable as a deterministic command.
- Repository support policy (v1) targets:
  - Python (`python3`) for deterministic tooling
  - Node.js (`node`) for cross-platform scripts
  - POSIX shell (`sh`) for thin wrappers

### 2.5 Test Execution Model (CI-friendly)
- Every Skill must include offline tests and fixtures.
- Required checks:
  - Validate `skill.yaml` against `skills/_schema/skill.schema.json`.
  - Validate stdin/stdout JSON against the Skill’s input/output schemas.
  - Execute Skill tests without network access and without time-based assertions.

## 3. Canonical Skill Contract

### 3.1 `skill.yaml` Contract (v1)
This repository standardizes on YAML for human authoring and JSON Schema for validation.

```yaml
apiVersion: skill/v1
kind: Skill

id: schema.validate_json
name: Validate JSON
version: 1.0.0
description: Validate input JSON against a provided JSON Schema.

governance:
  specId: "6f34688b-a76e-46b8-8d2d-8ffe5c88f9c6"
  oneSkillPerCommit: true
  concepts: []
  synchronizations: []

runtime:
  type: command
  command:
    - python3
    - impl/run.py
  cwd: "."
  timeoutMs: 60000

io:
  inputSchema: schemas/input.schema.json
  outputSchema: schemas/output.schema.json
  input:
    transport: stdin
    encoding: json
  output:
    transport: stdout
    encoding: json

determinism:
  network: forbidden
  time: forbidden
  randomness: forbidden

security:
  access:
    filesystem:
      read: []
      write: []
    env:
      read: []
    subprocess:
      allowed: false
    network:
      allowed: false

observability:
  logs:
    format: jsonl
    destination: stderr
  runReport:
    enabled: true

x-notes: {}
```

### 3.2 Required Fields (normative)
- `apiVersion`, `kind`: contract versioning and parsing.
- `id`, `name`, `version`, `description`: stable addressing and discovery.
- `governance.specId`: PDCA traceability (required).
- `runtime`: executable entrypoint (required) and must be relative to the Skill directory.
- `io.inputSchema`, `io.outputSchema`: schema-defined I/O (required).
- `determinism.*`: explicit determinism constraints (required).
- `security.access`: explicit access declaration (required).
- `observability`: log and run-report contract (required).

### 3.3 Allowed Extensions
- Only `x-*` top-level keys are allowed for extensions.
- Extensions must be non-executable metadata; execution behavior must remain in the contract fields above.

### 3.4 Schema Validation Rules (normative)
- Reject unknown keys unless `x-*`.
- Reject absolute paths and any `..` path segments in `runtime.command` and schema paths.
- If `determinism.network=allowed`, then `security.access.network.allowed` must be `true` and a Security approval reference must exist (e.g., `x-securityApprovalId`).
- Skills must declare stdin/stdout JSON transport; side channels for data exchange are forbidden.

### 3.5 Contract Mapping (Codex / MCP / CLI)
- Codex/GPT/Claude: select `skill.id`, produce JSON input, orchestrator executes the Skill command and validates output schema.
- CLI: `skillctl run <skill.id>` is the canonical interface (runner is a thin adapter around `runtime.command` + schema checks).
- MCP: expose each Skill as an MCP tool:
  - `tool.name = skill.id`
  - `tool.description = skill.description`
  - `tool.inputSchema = skill.io.inputSchema` (loaded contents)
  - `tool.outputSchema = skill.io.outputSchema` (loaded contents)
  - `tool.handler = skillctl run <skill.id>`

## 4. Codex Skill Conversion Prompt (Final)

Locked template (must be used for upstream conversions):

```
You are converting an upstream “skill/tool” into a deterministic Skill package.

INPUTS:
- Upstream source (code/spec/docs): <PASTE>
- Target skill id: <skill.id>
- Target skill slug: <skills/<slug>>
- Governing Spec ID: <SPEC-...>

OUTPUT:
- Produce a repo patch that adds exactly one new directory: skills/<slug>/
- Include: skill.yaml, schemas/input.schema.json, schemas/output.schema.json, impl/*, tests/*, fixtures/*

RULES (NON-NEGOTIABLE):
- No prompts anywhere in implementation.
- No LLM calls, no network I/O.
- Deterministic: no reading system time; no randomness unless seeded via input.
- Stateless: no persistence outside declared filesystem write globs.
- All I/O via JSON stdin/stdout only.
- Add tests that pass offline and validate output schema.
- If upstream cannot be made compliant, output ONLY: “REJECTED: <reason>”.
```

## 5. Upstream Skill Ingestion Policy

### 5.1 Global Rules
- Allowed:
  - Deterministic tools with explicit inputs/outputs
  - Declarative tool specs that can be implemented without prompts/LLM calls
- Rejected:
  - Prompt-only “skills”, agent chains, memory/planning logic
  - Any default network dependence without Security-approved connectors
- Required transformations:
  - Normalize to `skills/<slug>/` package layout
  - Provide `skill.yaml` + JSON Schemas + offline tests/fixtures
  - Remove vendor SDK coupling from the runtime execution path

### 5.2 Source-specific Policy
- OpenAI Codex Skills: accept only code-backed tools; reject prompt-only flows.
- Anthropic Skills: accept only code-backed tools; reject semantic/prompt units.
- Microsoft Semantic Kernel: accept native/plugins; reject semantic functions.
- LangChain tools: accept `StructuredTool`-like wrappers only if underlying function is deterministic; reject chains/agents/LLM-calling tools.
- MCP servers: accept only offline/local tools or Security-approved connectors; otherwise re-implement locally as a Skill.

## 6. Foundational Skill Taxonomy (v1)

Prioritized bootstrap set (atomic, cross-domain, no business logic):
- `skill.validate_manifest` — validate `skill.yaml` against `skills/_schema/skill.schema.json`.
- `schema.validate_json` — validate JSON against a JSON Schema.
- `fs.hash_tree` — deterministic hashing of a directory tree for caching and change detection.
- `workflow.create_revision_snapshot` — create local `ai_workflow_revisions/rev_n_current` snapshots deterministically (gitignored by default).
- `security.scan_secrets` — offline secret scanning with a deterministic report.

## 7. Framework Integration Map

Mechanical interactions:
- Concepts:
  - Call Skills only via the canonical runner interface (or directly via `runtime.command`), treating Skills as external deterministic tools.
  - Never embed Skill implementations in Concept code.
- Synchronizations:
  - Required when a Skill’s side effects span multiple Concepts; reference the Synchronization contract in `skill.yaml:governance.synchronizations`.
- Planner / Task Manager:
  - Select `skill.id`, produce JSON input, execute Skill, store run evidence in ledgers and PDCA artifacts.
- Security Agent:
  - Gate network/subprocess/filesystem/env access using `skill.yaml:security.access` and the repo Access Manifest.
- Observability Agent:
  - Consume required run reports and structured logs for metrics and alerting.
- Caching Agent:
  - Cache outputs only when determinism constraints allow (no time/random/network) and all reads are declared.

## 8. Open Risks & Mitigations
- Risk: Skill runner dependencies drift across environments (schema validation tooling).
  - Mitigation: pin tooling versions in CI; keep runner dependency surface small.
- Risk: Determinism claims are violated by hidden reads/time/randomness.
  - Mitigation: enforce strict access declarations, offline tests/fixtures, and optional sandboxing for runtime enforcement.
- Risk: Skill packages become de facto business logic.
  - Mitigation: require Concepts/Synchronizations for business logic and treat Skills as shared infrastructure only.

## 9. Tooling: `skillctl`

This repo provides a deterministic runner to validate and execute Skills:
- Script: `scripts/skillctl`
- Setup: run `scripts/setup-skillctl-venv.sh` to create `.venv-skillctl/` (configurable via `SKILLCTL_VENV`).
- Dependency: `jsonschema` (used for contract and I/O schema validation); `skill.yaml` parsing uses a restricted YAML subset parser in `scripts/skillctl.py`.

Supported commands (v1):
- `scripts/skillctl list`
- `scripts/skillctl describe <skill.id>`
- `scripts/skillctl validate --all`
- `scripts/skillctl run <skill.id> --input <file.json>`

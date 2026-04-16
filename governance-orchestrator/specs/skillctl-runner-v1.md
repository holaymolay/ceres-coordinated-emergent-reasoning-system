Spec Title: skillctl Runner v1 (Deterministic Skill Execution)
Spec ID: b6339a16-f334-4d1a-9349-b1ba167a6c3e
User Story: As an execution agent or CLI user, I need a deterministic Skill runner so that Skills can be validated and executed offline with schema-defined I/O and enforceable governance.

Functional Requirements:
- Provide a CLI named `skillctl` with commands:
  - `list` (discover Skills)
  - `describe` (show Skill metadata)
  - `validate` (validate `skill.yaml` + referenced schemas)
  - `run` (execute a Skill with JSON stdin/stdout validation)
- Skill discovery:
  - Scan `skills/` for Skill package directories containing `skill.yaml`.
  - Ignore directories starting with `_`.
  - Support invocation by Skill ID (`skill.yaml:id`) or explicit path.
- Validation:
  - Parse `skill.yaml` as YAML.
  - Validate Skill manifest against `skills/_schema/skill.schema.json`.
  - Validate referenced `io.inputSchema` and `io.outputSchema` paths exist and are valid JSON.
- Execution:
  - Read input JSON from stdin (default) or `--input <file>`.
  - Validate input JSON against the Skill’s input schema.
  - Execute `runtime.command` with cwd rooted in the Skill directory (optionally with `runtime.cwd`).
  - Parse stdout as JSON; validate against the Skill’s output schema.
  - Emit canonical JSON to stdout (normalized serialization).
  - Emit a run report to stderr as a single JSON line (JSONL), including timing and status.

Non-functional Requirements:
- Deterministic: `skillctl` must not call any LLMs and must not require network access.
- Portability: `skillctl` must run on standard developer/CI environments using stable tooling.
- Testability: include an offline smoke test that runs `skillctl validate` and `skillctl run` against at least one Skill fixture.

Architecture Overview:
- `skillctl` is a thin deterministic wrapper around:
  - YAML loading of `skill.yaml`
  - JSON Schema validation of contract and I/O
  - Subprocess execution of the Skill runtime command
  - Structured run reporting
- `skillctl` does not embed prompts, memory, planning, or questioning logic.

Language & Framework Requirements:
- Implement `skillctl` in Python 3 using minimal dependencies.
- Provide a setup script to create an isolated virtualenv for dependencies (`scripts/setup-skillctl-venv.sh`).

Testing Plan:
- Add a test script under `tests/` that:
  - Validates the `skills/_template/skill.yaml` using `skillctl validate` (as a contract smoke check).
  - Runs a sample Skill (added separately) using `skillctl run` and asserts output.

Dependencies:
- YAML parsing for `skill.yaml` must be supported without requiring an LLM; `skillctl` may implement a restricted YAML subset parser to avoid external YAML dependencies.
- JSON Schema validation library (pin in tooling if needed).

Input/Output Schemas:
- Input: JSON via stdin or `--input`.
- Output: JSON via stdout; run report JSON via stderr.

Validation Criteria:
- `skillctl list/describe/validate/run` operate correctly in a clean checkout with offline fixtures.
- `skillctl validate` fails fast and clearly on schema/path issues.
- `skillctl run` rejects non-JSON stdout and invalid output schema.

Security Constraints:
- No outbound network calls.
- Do not log secrets from inputs; avoid echoing raw input on failures.
- Execute only relative `runtime.command` entries within the Skill directory tree.

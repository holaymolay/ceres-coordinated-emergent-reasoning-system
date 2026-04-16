Spec Title: Skill skillcard.parse v1 (Parse SKILL.md Frontmatter)
Spec ID: b1ff11cb-dc41-4fc9-aaff-c23a2ad7ea86
User Story: As an execution agent or CLI user, I need a deterministic way to parse and validate SKILL.md frontmatter so upstream Skill Card repositories (Anthropic/Claude Skills, OpenAI Codex Skills) can be inspected and migrated into executable Skills.

Functional Requirements:
- Provide a Skill `skillcard.parse` that:
  - Accepts either a relative file path to a `SKILL.md` file or the raw markdown text.
  - Extracts YAML frontmatter key/value pairs (restricted to simple scalars).
  - Splits the markdown body (optional output).
  - Emits a structured JSON result on stdout.

Non-functional Requirements:
- Deterministic: output must be a pure function of provided inputs (and file contents when `path` is used); no timestamps, no randomness, no network.
- Stateless: no persistence outside stdout.
- Portable: Python 3 standard library only.

Architecture Overview:
- Minimal frontmatter parser for the subset used by upstream `SKILL.md` specs (key/value scalar pairs).
- Profile-based validation for common constraints (compatibility profile vs Anthropic vs OpenAI Codex limits).

Testing Plan:
- Add fixtures with a valid and invalid `SKILL.md` and a smoke test that asserts stable output JSON.

Input/Output Schemas:
- Input (JSON):
  - `path` (string, optional): relative path to `SKILL.md` (no absolute paths, no `..`).
  - `text` (string, optional): raw `SKILL.md` markdown.
  - `includeBody` (boolean, optional): include body text in output (default false).
  - `profile` (string, optional): validation profile (default `compat`).
- Output (JSON):
  - `ok` (boolean)
  - `frontmatter` (object)
  - `errors` (array)
  - `warnings` (array)
  - `body` (string|null)

Validation Criteria:
- Skill output is stable for the same inputs.
- Smoke test passes offline.

Security Constraints:
- No network access.
- Filesystem reads must be explicitly declared in `skill.yaml` and limited to `**/SKILL.md`.

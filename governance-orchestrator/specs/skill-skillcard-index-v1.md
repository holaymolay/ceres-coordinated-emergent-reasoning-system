Spec Title: Skill skillcard.index v1 (Index SKILL.md Skill Cards)
Spec ID: 354620f4-e4c8-4d64-89da-a58bbfec8ef6
User Story: As an execution agent or CLI user, I need a deterministic way to discover and summarize `SKILL.md` Skill Cards so I can build catalogs from upstream sources and present a comprehensive, searchable list to agents.

Functional Requirements:
- Provide a Skill `skillcard.index` that:
  - Recursively scans a provided root directory for files named `SKILL.md`.
  - Parses YAML frontmatter key/value pairs (restricted to simple scalars).
  - Validates required fields (`name`, `description`) and basic format constraints via a selected profile.
  - Emits a stable JSON index on stdout.

Non-functional Requirements:
- Deterministic: output must be a pure function of the scanned `SKILL.md` files and selected options; no timestamps, no randomness, no network.
- Stateless: no persistence outside stdout.
- Portable: Python 3 standard library only.

Architecture Overview:
- Deterministic traversal using `os.walk` with sorted directory and file lists.
- Reuse the same restricted YAML subset parsing rules as `skillcard.parse`.

Testing Plan:
- Provide fixtures with multiple `SKILL.md` files and an offline smoke test that asserts stable output JSON (ignoring machine-specific absolute root paths).

Input/Output Schemas:
- Input (JSON):
  - `root` (string, required): directory to scan.
  - `profile` (string, optional): validation profile (`compat` default).
  - `maxResults` (integer, optional): cap the number of discovered skillcards.
- Output (JSON):
  - `root` (string): resolved absolute path.
  - `profile` (string)
  - `total` (integer)
  - `valid` (integer)
  - `invalid` (integer)
  - `skillcards` (array): per-file parse and validation results.

Validation Criteria:
- Output is stable across runs with the same inputs/files.
- Smoke test passes offline.

Security Constraints:
- No network access.
- Filesystem reads must be explicitly declared in `skill.yaml`.

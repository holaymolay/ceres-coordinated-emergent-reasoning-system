Spec Title: OpenAI Skills Sync v1 (Curated Skill Install)
Spec ID: df326da2-d41a-4f1e-bdf6-d8b74db4434d
User Story: As a workflow operator, I need to sync curated OpenAI skills into the local Codex skill registry so updates are incorporated and auditable.

Functional Requirements:
- Fetch the curated skill list from `openai/skills` (`skills/.curated`) via the skill-installer workflow.
- Install missing curated skills into `$CODEX_HOME/skills` without overwriting existing installs.
- Record the sync result in `completed.md`, `CHANGELOG.md`, and `handover.md`.
- Keep repo state consistent with governance (ledger entry + pre/post inbox sweep).

Non-functional Requirements:
- Network access is required only for fetching the curated list and downloading skill sources.
- Fail closed on any install error; do not partially overwrite existing skills.
- No repository code changes beyond specs/logs/ledger unless explicitly requested.

Architecture Overview:
- Use the system Skill `skill-installer` to list and install skills from `openai/skills`.
- Installation target is `$CODEX_HOME/skills`; repo changes capture audit records only.

Language & Framework Requirements:
- Use the provided Python scripts under `~/.codex/skills/.system/skill-installer/scripts/`.

Testing Plan:
- Run the curated list command and verify output parses.
- Verify installed skill directories exist under `$CODEX_HOME/skills`.

Dependencies:
- Network access to GitHub.
- Existing Codex skill installer scripts.

Input/Output Schemas:
- Curated list output format from `list-curated-skills.py --format json`.

Validation Criteria:
- All missing curated skills are installed successfully without overwriting existing installs.
- Audit entries are logged in `completed.md`, `CHANGELOG.md`, and `handover.md`.

Security Constraints:
- No credentials are embedded; rely on existing GitHub access.
- Installation paths are validated by the installer; no arbitrary writes outside `$CODEX_HOME/skills`.

# Skill Ideas (Brainstorm List)

This is a non-authoritative brainstorming list of potential reusable Skills to build over time. It is not a spec and does not indicate that any of these Skills exist yet.

Conventions:
- Skill IDs use dot-namespace + snake segments (example: `fs.hash_tree`).
- Keep Skills atomic, deterministic, and cross-domain where possible; anything requiring network/subprocess access should be explicitly gated by `skill.yaml:security.access` and review.

## Core Validation & Contracts
- `skill.validate_manifest` — Validate a `skill.yaml` file against `skills/_schema/skill.schema.json`.
- `schema.validate_json` — Validate JSON against a provided JSON Schema (pure function; no network).
- `schema.normalize_json` — Canonicalize JSON (sorted keys, normalized whitespace) for stable diffs/caching.
- `schema.extract_json_pointer` — Extract a value from JSON by JSON Pointer path.
- `schema.apply_json_patch` — Apply RFC 6902 JSON Patch deterministically.

## Skill Card / Metadata Ingestion
- `skillcard.fetch_repo` — Fetch a pinned upstream Skill Card repo (commit SHA) into a local cache directory (network-gated).
- `skillcard.index_repo` — Index a repo tree into a catalog JSON (builds on `skillcard.index`).
- `skillcard.convert_to_skill_spec` — Convert a `SKILL.md` card into a deterministic Skill *spec stub* (not an implementation).
- `catalog.merge` — Merge multiple skill catalogs into one deterministic registry with stable ordering.
- `catalog.search` — Query a catalog by keyword/tags and return top matches deterministically.

## Filesystem & Text Utilities
- `fs.find` — List files matching include/exclude globs with stable ordering.
- `fs.read_text` — Read a text file with encoding detection rules; return content + metadata.
- `fs.write_text` — Write a text file with explicit newline/encoding options (write-gated).
- `fs.copy_tree` — Deterministically copy a directory tree with include/exclude rules.
- `fs.delete_paths` — Delete specific paths (write-gated; destructive).
- `fs.diff_tree` — Compare two directory trees and emit a structured diff.
- `fs.line_endings_normalize` — Normalize CRLF/LF across matched files (write-gated).
- `text.grep` — Deterministic text search across files (like `rg`, but structured JSON output).
- `text.replace` — Apply deterministic search/replace operations (write-gated; with dry-run mode).

## Git / Repo Skills
- `git.status_summary` — Parse `git status --porcelain` into structured JSON.
- `git.diff_summary` — Produce a stable summary of `git diff` (changed files, hunks, stats).
- `git.blame_lines` — Return blame info for a file + line range.
- `git.find_introduced_by` — Locate the commit that introduced a string/pattern.
- `git.tag_next_version` — Compute the next semver tag given a strategy (no tagging unless approved).

## Security & Compliance
- `security.scan_secrets` — Offline secret scanning with deterministic findings (paths + match types).
- `security.scan_private_keys` — Detect private key material and common credential formats.
- `security.scan_dependencies` — Parse lockfiles and summarize dependency versions (stack-aware).
- `security.hash_artifact` — Hash an artifact (file/dir) and emit a signed/structured manifest (signing gated).
- `security.verify_hash_manifest` — Verify an artifact against a hash manifest.

## Testing / Quality Automation
- `qa.run_command` — Run a command and return structured output (subprocess-gated; deterministic formatting).
- `qa.parse_junit` — Parse JUnit XML into a stable summary.
- `qa.parse_coverage` — Parse coverage reports into a stable summary.
- `lint.format_check` — Run formatter in check mode and summarize diffs (tooling-gated).
- `lint.lint_check` — Run linter and normalize findings into stable JSON.

## Docs / Markdown
- `md.toc_generate` — Generate a table of contents for a markdown file deterministically.
- `md.link_check` — Validate relative links and anchors offline.
- `md.extract_code_blocks` — Extract fenced code blocks by language into JSON (for reuse/tests).
- `md.frontmatter_parse` — Parse YAML frontmatter for markdown docs (restricted subset).
- `docs.changelog_entry` — Generate a changelog entry given an explicit timestamp and summary (time via input).

## Data Transformation (Offline)
- `data.csv_to_json` — Convert CSV to JSON with explicit delimiter/quote rules.
- `data.json_to_csv` — Convert JSON array to CSV with explicit column ordering.
- `data.sqlite_query` — Run read-only SQLite queries and emit JSON (filesystem read + subprocess/tooling gated).
- `data.redact_fields` — Deterministically redact configured fields from JSON/text.
- `data.sample_rows` — Deterministic sampling given a seed in input (randomness: seeded).

## Network-Gated Connectors (Optional, Requires Security Approval)
- `net.http_get` — HTTP GET with allowlisted domains and explicit timeout (network-gated).
- `net.http_post_json` — HTTP POST JSON with allowlisted domains (network-gated).
- `net.download_file` — Download to a declared write path (network + filesystem write gated).
- `vcs.github_issues_list` — List GitHub issues via token env var (network + env read gated).
- `vcs.github_pr_create` — Create a PR (network + env read + write gated; high risk).

## Workflow / Governance Helpers
- `workflow.create_revision_snapshot` — Wrap `scripts/create-workflow-revision.sh` in a deterministic Skill interface.
- `workflow.todo_sweep_suggest` — Suggest reworded todos from `todo-inbox.md` (no writes; emits proposals).
- `workflow.spec_scaffold` — Scaffold a spec file with required headings and IDs.
- `workflow.handover_update_suggest` — Suggest handover updates based on provided deltas (no writes).
- `workflow.release_notes_generate` — Generate release notes from explicit inputs (no git/network; deterministic formatting).

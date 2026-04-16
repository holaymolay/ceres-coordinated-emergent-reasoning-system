Spec Title: Skill fs.hash_tree v1 (Deterministic Directory Hashing)
Spec ID: f67e6ec0-1c06-451d-9edb-7a2b7951772c
User Story: As an execution agent or CLI user, I need a deterministic way to hash a directory tree so that caching, change detection, and artifact integrity checks can be done without any LLM.

Functional Requirements:
- Provide a Skill `fs.hash_tree` that:
  - Accepts a root directory path and hashing algorithm.
  - Traverses the directory tree deterministically (sorted order).
  - Computes a per-file digest and a single tree digest derived from (relative path + file digest).
  - Emits JSON on stdout only.

Non-functional Requirements:
- Deterministic: output must be a pure function of file contents and paths (no timestamps, no randomness, no network).
- Stateless: no persistence outside stdout.
- Testable: include an offline fixture tree and a smoke test asserting the expected digests.

Architecture Overview:
- Implementation in Python using `hashlib` and deterministic traversal (`os.walk` with sorting).
- Exclude patterns apply to POSIX-style relative paths.

Language & Framework Requirements:
- Python 3 standard library only.

Testing Plan:
- Add `skills/fs-hash-tree/tests/test_smoke.sh` that runs the Skill against `skills/fs-hash-tree/fixtures/tree/` and compares stdout to `fixtures/output.expected.json`.

Input/Output Schemas:
- Input (JSON):
  - `root` (string, required): directory to hash (absolute or relative to runtime cwd).
  - `algorithm` (string, optional): hashing algorithm (default `sha256`).
  - `exclude` (array of strings, optional): glob patterns to exclude, matched against POSIX relative paths.
- Output (JSON):
  - `algorithm` (string)
  - `root` (string)
  - `treeDigest` (string hex)
  - `fileCount` (integer)
  - `files` (array of `{path,digest,size}`)

Validation Criteria:
- Skill emits stable digests across runs for the same inputs/files.
- Skill test passes offline.

Security Constraints:
- No network access.
- Filesystem reads must be explicitly declared in `skill.yaml`.

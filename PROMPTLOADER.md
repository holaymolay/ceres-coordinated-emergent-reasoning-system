# PROMPTLOADER.md
Status: Authoritative bootstrap entrypoint (non-interactive, deterministic).

Umbrella name: **CERES — Coordinated Emergent Reasoning System**.

## Non-Interactive Rule
Do not ask questions. Do not present options. Execute the bootstrap procedure and proceed.

## Procedure (run in order)
1) Fast init from URL (no git clone; extract only required files):

```bash
curl -fsSL https://codeload.github.com/holaymolay/ceres-coordinated-emergent-reasoning-system/tar.gz/master -o /tmp/ceres.tgz
python - <<'PY'
import json, tarfile, sys, os
from pathlib import Path

tar_path = Path("/tmp/ceres.tgz")
dest = Path(".").resolve()
with tarfile.open(tar_path, "r:*") as tar:
    members = tar.getmembers()
    root = members[0].name.split("/")[0]
    manifest_member = f"{root}/scripts/fast-init-manifest.json"
    manifest_file = tar.extractfile(manifest_member)
    if manifest_file is None:
        raise SystemExit("fast-init-manifest.json not found in tarball")
    manifest = json.loads(manifest_file.read().decode("utf-8"))
    paths = set(p.strip("/") for p in manifest.get("paths", []))
    prefix = root + "/"
    for member in members:
        name = member.name
        if not name.startswith(prefix):
            continue
        rel = name[len(prefix):].lstrip("/")
        if not rel or rel.startswith("..") or "/.." in rel:
            continue
        top = rel.split("/", 1)[0]
        if top in paths or rel in paths:
            member.name = rel
            tar.extract(member, path=dest)
PY
```

2) Run autobootstrap (must succeed without questions):

```bash
./.ceres/bin/autobootstrap
```

3) Ensure these exist (create/repair silently if missing):
- `.ceres/core`
- `.ceres/bin`
- `.ceres/components`
- `.ceres/workspace/todo-inbox.md`
- `.ceres/workspace/todo.md`
- `.ceres/workspace/completed.md`
- `.ceres/workspace/memory.md`
- `.ceres/workspace/handover.md`
- `.ceres/workspace/objective-contract.json`
- `.ceres/workspace/gap-ledger.json`
- `.ceres/workspace/specs/elicitation/elicitation.md`

4) Start session watcher (non-interactive):
- `./.ceres/bin/start-session`

5) Proceed directly to the first project prompt using:
- `prompts/plan.md` (Spec Elicitation + planning + execution start)

Verification prompt (when asked to confirm readiness):
- `prompts/prompt-ceres-verify.md`

Routing rule:
- If the user says "verify CERES is loaded/ready" (or equivalent), immediately execute `prompts/prompt-ceres-verify.md` with no questions.

## Required Defaults (FAST_START)
- execution_allowed = true
- enforcement = warn
- intake_required = auto_generate
- spec_elicitation = auto_generate_skeleton
- prompt_debugger = non_blocking
- gap_ledger = auto_append

## Constitutional Override
If `CONSTITUTION.md` exists, it must follow the non-interactive, auto-generate-and-proceed contract above.

CERES READY — next prompt should describe the project.

# CERES Upgrade

You are an LLM agent operating inside a project that uses CERES. The user has asked you to upgrade CERES to the latest version. Follow these instructions without asking questions.

## What changed

CERES has been consolidated from a multi-repo ecosystem into a single monorepo. Components that were previously separate repositories (governance-orchestrator, readme-spec-engine, spec-compiler, ui-constitution, ui-pattern-registry, parallel-agent-runner) now live inside the main CERES repo. The upgrade also adds LLM-agnostic harness detection, a compact STATE digest for small-context models, and updated bootstrap with a capability-detected fallback chain.

## Upgrade procedure

### Option A: Run the migration script (preferred)

Download and execute the migration script. It handles all cases (submodule, tarball, fresh install), preserves your `.ceres/workspace/`, and is safe to re-run.

```bash
curl -fsSL https://raw.githubusercontent.com/holaymolay/ceres-coordinated-emergent-reasoning-system/master/scripts/migrate-project.sh -o /tmp/ceres-migrate.sh
chmod +x /tmp/ceres-migrate.sh
bash /tmp/ceres-migrate.sh "$PWD"
```

Then verify:

```bash
./.ceres/bin/autobootstrap
```

### Option B: Manual steps (if the script cannot be downloaded)

If you cannot download the script, perform these steps in order:

1) **Back up workspace** (preserves your project's CERES state):
```bash
cp -a .ceres/workspace /tmp/ceres-workspace-backup
```

2) **Remove old core** (handles submodule or plain directory):
```bash
git submodule deinit .ceres/core 2>/dev/null || true
git rm --cached .ceres/core 2>/dev/null || true
git config --remove-section "submodule..ceres/core" 2>/dev/null || true
rm -rf .git/modules/.ceres/core 2>/dev/null || true
rm -rf .ceres/core
rm -f .ceres/core.lock
```

3) **Remove old components** (now part of core):
```bash
rm -rf .ceres/components
```

4) **Clean .gitmodules** (remove .ceres/core entry if present; delete file if empty):
```bash
if [ -f .gitmodules ]; then
  python3 -c "
import re, os, sys
p = '.gitmodules'
t = open(p).read()
t = re.sub(r'\[submodule \".ceres/core\"\][^\[]*', '', t, flags=re.DOTALL).strip()
if t: open(p,'w').write(t+'\n')
else: os.remove(p)
" 2>/dev/null || true
fi
```

5) **Install new core from monorepo**:
```bash
git clone --depth 1 https://github.com/holaymolay/ceres-coordinated-emergent-reasoning-system.git .ceres/core
```

6) **Re-run bootstrap**:
```bash
bash .ceres/core/scripts/bootstrap-workspace.sh --root "$PWD"
```

7) **Restore workspace** (bootstrap won't overwrite existing files, but this ensures nothing was lost):
```bash
cp -an /tmp/ceres-workspace-backup/* .ceres/workspace/ 2>/dev/null || true
```

8) **Add harness pointer files** (if not already present):
```bash
for f in CLAUDE.md GEMINI.md .cursorrules; do
  [ -f "$f" ] || echo "This project uses CERES. Read AGENTS.md for governance rules and PROMPTLOADER.md for bootstrap." > "$f"
done
```

9) **Run harness detection and state digest**:
```bash
CERES_WORKSPACE=.ceres/workspace python3 .ceres/core/scripts/detect-harness.py 2>/dev/null || true
CERES_WORKSPACE=.ceres/workspace python3 .ceres/core/scripts/generate-state-digest.py 2>/dev/null || true
```

10) **Update .gitignore** (add if not already present):
```bash
grep -q "^\.ceres/core/" .gitignore 2>/dev/null || echo -e "\n.ceres/core/\n.ceres/core.lock" >> .gitignore
```

11) **Verify**:
```bash
./.ceres/bin/autobootstrap
```

## Post-upgrade

After a successful upgrade:
- `.ceres/core/` contains the full CERES monorepo (all components included)
- `.ceres/workspace/` is unchanged (your project state is preserved)
- `.ceres/bin/` has updated wrappers
- `CLAUDE.md`, `GEMINI.md`, `.cursorrules` exist as harness pointer files
- `.ceres/workspace/harness.json` identifies your LLM harness
- `.ceres/workspace/STATE.md` provides a compact state digest

Report: "CERES upgraded to monorepo version. Workspace preserved. Run `.ceres/bin/autobootstrap` to verify."

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

parse_repos() {
python - <<'PY'
import pathlib
path = pathlib.Path('repos.yaml')
data = []
current = None
for raw in path.read_text().splitlines():
    line = raw.strip()
    if not line or line.startswith('#'):
        continue
    if line.startswith('- '):
        if current:
            data.append(current)
        current = {}
        line = line[2:]
        if line and ':' in line:
            k, v = line.split(':', 1)
            current[k.strip()] = v.strip()
        continue
    if current is not None and ':' in line:
        k, v = line.split(':', 1)
        current[k.strip()] = v.strip()
if current:
    data.append(current)
for repo in data:
    name = repo.get('name') or ''
    path = repo.get('local_path') or ''
    print(f"{name}\t{path}")
PY
}

echo "Umbrella repo: $ROOT"
um_branch=$(git -C "$ROOT" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
um_branch=${um_branch:-n/a}
um_sha=$(git -C "$ROOT" rev-parse --short HEAD 2>/dev/null || true)
um_sha=${um_sha:-n/a}
um_dirty=$(git -C "$ROOT" status --porcelain | grep -q . && echo dirty || echo clean)
printf '  branch: %s | sha: %s | %s\n' "$um_branch" "$um_sha" "$um_dirty"

printf '\nComponent repos:\n'
while IFS=$'\t' read -r name rel_path; do
  [[ -z "$name" ]] && continue
  repo_path="$ROOT/$rel_path"
  if [[ ! -d "$repo_path" ]]; then
    printf '  %s: MISSING at %s\n' "$name" "$repo_path"
    continue
  fi
  branch=$(git -C "$repo_path" rev-parse --abbrev-ref HEAD 2>/dev/null || true)
  branch=${branch:-n/a}
  sha=$(git -C "$repo_path" rev-parse --short HEAD 2>/dev/null || true)
  sha=${sha:-n/a}
  status=$(git -C "$repo_path" status --porcelain | grep -q . && echo dirty || echo clean)
  printf '  %s: branch=%s | sha=%s | %s\n' "$name" "$branch" "$sha" "$status"
done < <(parse_repos)

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

while IFS=$'\t' read -r name rel_path; do
  [[ -z "$name" ]] && continue
  repo_path="$ROOT/$rel_path"
  if [[ ! -d "$repo_path" ]]; then
    printf 'WARN: %s missing at %s\n' "$name" "$repo_path"
    continue
  fi
  printf 'Syncing %s at %s\n' "$name" "$repo_path"
  git -C "$repo_path" fetch --all --prune
  git -C "$repo_path" pull --ff-only
done < <(parse_repos)

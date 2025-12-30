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
    print(name)
PY
}

readarray -t doc_files < <(find "$ROOT" -maxdepth 1 -name 'README.md' -o -path "$ROOT/docs/*.md")
missing=0
for name in $(parse_repos); do
  [[ -z "$name" ]] && continue
  if ! grep -R -q -- "$name" "${doc_files[@]}"; then
    printf 'Missing reference: %s\n' "$name"
    missing=1
  fi
done

if [[ $missing -ne 0 ]]; then
  echo "Link verification failed"
  exit 1
fi

echo "All component names found in umbrella docs."

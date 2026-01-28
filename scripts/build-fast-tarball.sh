#!/usr/bin/env bash
set -euo pipefail

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MANIFEST="${1:-$ROOT/scripts/fast-init-minimal.json}"
OUT_DIR="${2:-$ROOT/dist}"
OUT_TAR="${3:-$OUT_DIR/ceres-fast.tar.gz}"

mkdir -p "$OUT_DIR"

python3 - <<'PY' "$ROOT" "$MANIFEST" "$OUT_TAR"
import json
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
manifest = Path(sys.argv[2])
out_tar = Path(sys.argv[3])

data = json.loads(manifest.read_text(encoding="utf-8"))
paths = [p.strip("/") for p in data.get("paths", []) if isinstance(p, str)]
if not paths:
    raise SystemExit("Manifest has no paths.")

prefix = "ceres-fast"
temp_dir = out_tar.parent / prefix
if temp_dir.exists():
    subprocess.run(["rm", "-rf", str(temp_dir)], check=False)
temp_dir.mkdir(parents=True, exist_ok=True)

for rel in paths:
    src = root / rel
    if not src.exists():
        continue
    dest = temp_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        subprocess.run(["cp", "-R", str(src), str(dest.parent)], check=False)
    else:
        subprocess.run(["cp", str(src), str(dest)], check=False)

if out_tar.exists():
    out_tar.unlink()

subprocess.run(["tar", "-czf", str(out_tar), "-C", str(out_tar.parent), prefix], check=True)
print(f"Wrote {out_tar}")
PY

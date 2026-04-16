#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

tmp_out="$(mktemp)"
trap 'rm -f "$tmp_out"' EXIT

(cd "$skill_dir" && python3 "impl/run.py" < "fixtures/input.json" > "$tmp_out")

python3 - "$skill_dir/fixtures/output.expected.json" "$tmp_out" <<'PY'
import json
import sys
from pathlib import Path

expected_path = Path(sys.argv[1])
actual_path = Path(sys.argv[2])

expected = json.loads(expected_path.read_text(encoding="utf-8"))
actual = json.loads(actual_path.read_text(encoding="utf-8"))

for key in ("root", "treeDigest"):
    if expected.get(key) in ("REPLACE_ME", None):
        expected.pop(key, None)
        actual.pop(key, None)

if expected != actual:
    print("Mismatch:", file=sys.stderr)
    print("expected:", expected, file=sys.stderr)
    print("actual:", actual, file=sys.stderr)
    raise SystemExit(1)
PY

#!/usr/bin/env bash
set -euo pipefail

skill_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

run_case() {
  local input_rel="$1"
  local expected_rel="$2"

  local tmp_out
  tmp_out="$(mktemp)"
  trap 'rm -f "$tmp_out"' RETURN

  (cd "$skill_dir" && python3 "impl/run.py" < "$input_rel" > "$tmp_out")

  python3 - "$skill_dir/$expected_rel" "$tmp_out" <<'PY'
import json
import sys
from pathlib import Path

expected_path = Path(sys.argv[1])
actual_path = Path(sys.argv[2])

expected = json.loads(expected_path.read_text(encoding="utf-8"))
actual = json.loads(actual_path.read_text(encoding="utf-8"))

if expected != actual:
    print("Mismatch:", file=sys.stderr)
    print("expected:", expected, file=sys.stderr)
    print("actual:", actual, file=sys.stderr)
    raise SystemExit(1)
PY
}

run_case "fixtures/valid/input.json" "fixtures/valid/output.expected.json"
run_case "fixtures/invalid/input.json" "fixtures/invalid/output.expected.json"

#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: scripts/compare-shell-python.sh <base-name> [-- args...]" >&2
  echo "Example: scripts/compare-shell-python.sh preflight -- --mode execute" >&2
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

base="$1"
shift

if [[ "$1" == "--" ]]; then
  shift
fi

ROOT="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
sh_script="$ROOT/scripts/${base}.sh"
py_script="$ROOT/scripts/${base}.py"

if [[ ! -f "$sh_script" ]]; then
  echo "Shell script not found: $sh_script" >&2
  exit 1
fi
if [[ ! -f "$py_script" ]]; then
  echo "Python script not found: $py_script" >&2
  exit 1
fi
if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required for comparison." >&2
  exit 1
fi

workdir="$(mktemp -d)"
trap 'rm -rf "$workdir"' EXIT

set +e
bash "$sh_script" "$@" >"$workdir/shell.out" 2>"$workdir/shell.err"
code_sh=$?
python3 "$py_script" "$@" >"$workdir/python.out" 2>"$workdir/python.err"
code_py=$?
set -e

status=0
if [[ "$code_sh" -ne "$code_py" ]]; then
  echo "Exit code mismatch: shell=$code_sh python=$code_py" >&2
  status=1
fi

if ! cmp -s "$workdir/shell.out" "$workdir/python.out"; then
  echo "STDOUT mismatch:" >&2
  diff -u "$workdir/shell.out" "$workdir/python.out" >&2 || true
  status=1
fi

if ! cmp -s "$workdir/shell.err" "$workdir/python.err"; then
  echo "STDERR mismatch:" >&2
  diff -u "$workdir/shell.err" "$workdir/python.err" >&2 || true
  status=1
fi

if [[ "$status" -eq 0 ]]; then
  echo "OK: Outputs and exit codes match." >&2
fi

exit "$status"

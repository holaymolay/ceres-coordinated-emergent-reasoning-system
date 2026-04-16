#!/bin/sh
set -eu

root_dir="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
tmp_file="$(mktemp)"
trap 'rm -f "$tmp_file"' EXIT

sh "$root_dir/impl/run.sh" < "$root_dir/fixtures/input.json" > "$tmp_file"
diff -u "$root_dir/fixtures/output.expected.json" "$tmp_file"


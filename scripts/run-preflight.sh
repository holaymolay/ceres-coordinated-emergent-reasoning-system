#!/usr/bin/env bash
set -euo pipefail

scripts_dir="$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

"${scripts_dir}/check-git-state.sh"
"${scripts_dir}/check-invariants.sh"

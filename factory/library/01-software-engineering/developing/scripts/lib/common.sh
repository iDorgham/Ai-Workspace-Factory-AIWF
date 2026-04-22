#!/usr/bin/env bash
# Shared helpers for scripts under scripts/<category>/.
# shellcheck shell=bash
#
# Usage in a category script (first lines after shebang):
#   _GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   # shellcheck source=scripts/lib/common.sh
#   source "${_GALERIA_HERE}/../lib/common.sh"
#   ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

sovereign_repo_root() {
  local script_dir="${1:-}"
  if [[ -z "$script_dir" ]]; then
    printf '%s\n' "sovereign_repo_root: missing script directory" >&2
    return 1
  fi
  cd "${script_dir}/../.." && pwd
}

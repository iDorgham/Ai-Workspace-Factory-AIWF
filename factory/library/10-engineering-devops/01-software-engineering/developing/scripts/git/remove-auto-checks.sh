#!/usr/bin/env bash
# Turn off automatic code checks (the ones installed by install-auto-checks.sh).
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
GIT_HOOKS="${ROOT}/.git/hooks"

for name in pre-commit pre-push; do
  path="${GIT_HOOKS}/${name}"
  if [[ -f "$path" ]] && grep -q 'scripts/hooks/run-' "$path" 2>/dev/null; then
    rm -f "$path"
    printf '✓ Removed automatic check: %s\n' "$name"
  else
    printf '  Left unchanged: %s (not managed by Sovereign or already removed)\n' "$name"
  fi
done

printf '\n'
printf '%s\n' "Automatic checks are OFF."
printf '%s\n' "To turn them back on: bash scripts/git/install-auto-checks.sh"
printf '\n'

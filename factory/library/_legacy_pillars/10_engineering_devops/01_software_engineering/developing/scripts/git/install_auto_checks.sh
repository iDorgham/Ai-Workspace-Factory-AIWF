#!/usr/bin/env bash
# Turn on automatic code checks — runs a quick check every time you save (commit) or share (push) code.
# Run this once per clone. After that, it works automatically.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
GIT_DIR="${ROOT}/.git"

if [[ ! -d "$GIT_DIR" ]]; then
  printf '%s\n' "No .git folder found. Initialize git first: git init"
  exit 1
fi

write_hook() {
  local name="$1"
  local runner="$2"
  local path="${GIT_DIR}/hooks/${name}"
  printf '%s\n' \
    '#!/bin/sh' \
    'if [ "${SKIP:-}" = "1" ] || [ "${GALERIA_NO_HOOKS:-}" = "1" ]; then exit 0; fi' \
    'ROOT="$(git rev-parse --show-toplevel)"' \
    "exec \"\$ROOT/scripts/hooks/${runner}\"" \
    >"$path"
  chmod +x "$path"
  printf '✓ Installed automatic check: %s\n' "$name"
}

write_hook pre-commit run-pre-commit.sh
write_hook pre-push run-pre-push.sh

chmod +x "${ROOT}/scripts/hooks/run-pre-commit.sh" "${ROOT}/scripts/hooks/run-pre-push.sh" 2>/dev/null || true

printf '\n'
printf '%s\n' "Automatic checks are ON."
printf '%s\n' "  • When you commit: checks code style (fast, no install)"
printf '%s\n' "  • When you push:   same quick check (use PRE_PUSH_DEEP=1 for full check)"
printf '\n'
printf '%s\n' "To skip once:     SKIP=1 git commit   or   GALERIA_NO_HOOKS=1 git push"
printf '%s\n' "To turn off:      bash scripts/git/remove-auto-checks.sh"
printf '\n'

#!/usr/bin/env bash
# Git pre-push: quick-check by default; full-check when PRE_PUSH_DEEP=1.
# Skip: SKIP=1 or GALERIA_NO_HOOKS=1 git push ...
set -euo pipefail

if [[ "${SKIP:-}" == "1" ]] || [[ "${GALERIA_NO_HOOKS:-}" == "1" ]]; then
  exit 0
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -n "$ROOT" ]] || exit 0
cd "$ROOT"

if [[ "${PRE_PUSH_DEEP:-}" == "1" ]]; then
  printf '→ pre-push: PRE_PUSH_DEEP=1 — running full-check.sh\n'
  exec bash "$ROOT/scripts/check/full-check.sh"
fi

exec bash "$ROOT/scripts/check/quick-check.sh"

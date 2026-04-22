#!/usr/bin/env bash
# Git pre-commit: whitespace on staged diff + quick-check (lint or typecheck, no install).
# Skip entirely: SKIP=1 or GALERIA_NO_HOOKS=1 git commit ...
set -euo pipefail

if [[ "${SKIP:-}" == "1" ]] || [[ "${GALERIA_NO_HOOKS:-}" == "1" ]]; then
  exit 0
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -n "$ROOT" ]] || exit 0
cd "$ROOT"

if [[ -f "$ROOT/scripts/validate/runtime_state_guard.py" ]] && command -v python3 >/dev/null 2>&1; then
  if ! python3 "$ROOT/scripts/validate/runtime_state_guard.py" --critical-only; then
    printf '%s\n' "Runtime guard: critical drift (>=2) or failed-critical — fix sos/runtime-state.md or SKIP=1." >&2
    exit 1
  fi
fi

if ! git diff --cached --check >/dev/null 2>&1; then
  printf '%s\n' "Whitespace errors in staged changes:" >&2
  git diff --cached --check >&2 || true
  exit 1
fi

exec bash "$ROOT/scripts/check/quick-check.sh"

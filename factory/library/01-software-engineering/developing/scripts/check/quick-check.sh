#!/usr/bin/env bash
# Quick code check — runs fast, no install needed.
# Used by: git hooks, IDE tasks, or any time you want fast feedback.
# Skip: SKIP=1 git commit
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -n "$ROOT" ]] || exit 0
cd "$ROOT"

if [[ ! -f package.json ]]; then
  exit 0
fi

if ! command -v pnpm >/dev/null 2>&1; then
  printf '%s\n' "quick-check: pnpm not found. Install pnpm, then try again." >&2
  exit 1
fi

has_script() {
  node -e "const p=require('./package.json'); process.exit(p.scripts&&p.scripts['$1']?0:1)" 2>/dev/null
}

if has_script lint; then
  printf '→ Checking code style (lint)...\n'
  pnpm run lint
elif has_script typecheck; then
  printf '→ Checking types (typecheck)...\n'
  pnpm run typecheck
elif has_script type-check; then
  printf '→ Checking types (type-check)...\n'
  pnpm run type-check
else
  exit 0
fi

#!/usr/bin/env bash
# Report whether common Sovereign toolchain binaries are available (non-destructive).
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

code=0
printf 'Repository root: %s\n\n' "$ROOT"

if command -v git >/dev/null 2>&1; then
  printf '✓ git %s\n' "$(git --version)"
else
  printf '✗ git not found\n'
  code=1
fi

if command -v node >/dev/null 2>&1; then
  printf '✓ node %s\n' "$(node -v)"
else
  printf '✗ node not found\n'
  code=1
fi

if command -v pnpm >/dev/null 2>&1; then
  printf '✓ pnpm %s\n' "$(pnpm -v)"
else
  printf '○ pnpm not found (install before monorepo /init)\n'
fi

if command -v npx >/dev/null 2>&1; then
  printf '✓ npx available\n'
else
  printf '○ npx not found (usually ships with Node)\n'
fi

exit "$code"

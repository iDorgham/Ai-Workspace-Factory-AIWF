#!/usr/bin/env bash
# Full quality check — installs dependencies then runs all quality gates.
# Use before pushing important work or after a big change.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

if [[ ! -f package.json ]]; then
  printf '%s\n' "No project found yet. Run /init in your AI chat first to set up the project, then try again."
  exit 0
fi

if ! command -v pnpm >/dev/null 2>&1; then
  printf '%s\n' "pnpm is not installed. Install it from: https://pnpm.io/installation"
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  printf '%s\n' "Node.js is not installed. Install it from: https://nodejs.org"
  exit 1
fi

printf '→ Installing dependencies...\n'
pnpm install

has_script() {
  node -e "const p=require('./package.json'); process.exit(p.scripts&&p.scripts['$1']?0:1)" 2>/dev/null
}

run_script() {
  local name="$1"
  printf '→ Running %s...\n' "$name"
  pnpm run "$name"
}

if has_script quality; then
  run_script quality
elif has_script lint; then
  run_script lint
  if has_script typecheck; then
    run_script typecheck
  elif has_script type-check; then
    run_script type-check
  fi
elif [[ -f turbo.json ]] && command -v pnpm >/dev/null 2>&1; then
  if pnpm exec turbo run lint typecheck --continue 2>/dev/null; then
    :
  else
    printf '%s\n' "Some checks failed or are not configured. Run /init to complete project setup."
  fi
else
  printf '%s\n' "No quality checks configured yet. Run /init in your AI chat first, then this will work."
fi

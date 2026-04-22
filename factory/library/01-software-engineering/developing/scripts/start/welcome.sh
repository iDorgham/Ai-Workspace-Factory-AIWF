#!/usr/bin/env bash
# First-run friendly summary: tools, next steps, links (non-destructive).
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

printf '\n'
printf '%s\n' "Welcome to the Sovereign workspace."
printf '%s\n' "This template helps you plan and build an app with AI agents and quality gates."
printf '\n'

printf '%s\n' "── Your tools ──"
bash "${ROOT}/scripts/start/doctor.sh" || true
printf '\n'

if git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1; then
  printf '%s\n' "── Git ──"
  printf '  Repository: yes (good for hooks and branches)\n'
  printf '\n'
else
  printf '%s\n' "── Git ──"
  printf '  No .git folder here yet. Run: git init  (optional but recommended)\n'
  printf '\n'
fi

printf '%s\n' "── Suggested next steps ──"
printf '%s\n' "  1. Open docs/workspace/guides/ONBOARDING.md in your editor"
printf '%s\n' "  2. In your AI chat, run: /init (example: /init --type web --mode founder)"
printf '%s\n' "  3. Optional: pnpm run hooks:install  (catches issues before commit)"
printf '%s\n' "  4. See every command: pnpm run help"
printf '\n'

printf '%s\n' "── Product vs workspace docs ──"
printf '%s\n' "  Product (your idea):     docs/product/"
printf '%s\n' "  How Sovereign works:          docs/workspace/"
printf '\n'

#!/usr/bin/env bash
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

printf '\n'
printf '%s\n' "Step 1: Check your computer setup"
bash "${ROOT}/scripts/start/doctor.sh" || true
printf '\n'

printf '%s\n' "Step 2: Pick your starting path"
printf '%s\n' "- If you are new to this workspace, read:"
printf '%s\n' "  docs/workspace/guides/START_HERE_NON_DEVS.md"
printf '%s\n' "- If you want full technical details, read:"
printf '%s\n' "  docs/workspace/guides/ONBOARDING.md"
printf '\n'

printf '%s\n' "Step 3: Run your first command in AI chat"
printf '%s\n' "- Type: /init"
printf '%s\n' "- If you want non-technical language, type: /mode founder"
printf '\n'

printf '%s\n' "Step 4: Ask for your next exact command"
printf '%s\n' "- Run: bash scripts/start/guide.sh"
printf '\n'

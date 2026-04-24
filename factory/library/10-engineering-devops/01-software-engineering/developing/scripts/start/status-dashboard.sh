#!/usr/bin/env bash
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

STATUS_DIR="${ROOT}/docs/workspace/status"
STATUS_FILE="${STATUS_DIR}/PROJECT_STATUS.md"
ORCH_FILE="${ROOT}/.ai/plans/active/orchestration-state.json"

mkdir -p "${STATUS_DIR}"
mkdir -p "${ROOT}/.ai/plans/active"

today="$(date +%Y-%m-%d)"
phase="not-started"
blocked_reason="none"
owner_agent="@Guide"
last_gate="none"

if [[ -d "${ROOT}/.ai/plans/active/features" ]] && [[ -n "$(ls -A "${ROOT}/.ai/plans/active/features" 2>/dev/null || true)" ]]; then
  phase="planning-or-build"
fi

if [[ ! -d "${ROOT}/packages/shared/src/contracts" ]] || [[ -z "$(ls -A "${ROOT}/packages/shared/src/contracts" 2>/dev/null || true)" ]]; then
  blocked_reason="missing locked contracts"
fi

last_command="unknown"
log_file="${ROOT}/.ai/plans/active/audit/command-logs/${today}.md"
if [[ -f "${log_file}" ]]; then
  last_command="$(awk 'NF{last=$0} END{print last}' "${log_file}")"
fi

if [[ "${blocked_reason}" == "none" ]]; then
  last_gate="spec:validate"
fi

cat > "${ORCH_FILE}" <<JSON
{
  "currentPhase": "${phase}",
  "lastSuccessfulGate": "${last_gate}",
  "blockedReason": "${blocked_reason}",
  "ownerAgent": "${owner_agent}",
  "updatedAt": "${today}"
}
JSON

cat > "${STATUS_FILE}" <<MD
# Project Status

- Current phase: ${phase}
- Last command: ${last_command}
- Blockers: ${blocked_reason}
- Last successful gate: ${last_gate}
- Owner agent: ${owner_agent}
- Updated: ${today}

## Top Flows

1. Idea -> Spec (/plan)
2. Spec -> Build (/contract then /build)
3. Build -> Verify (/test then /quality all)
4. Verify -> Launch (/deploy)

## Beginner-safe presets

- build:beginner -> run /build with plain-language guidance
- quality:quick -> run /quality first
- deploy:dry-run -> run /deploy preview before production

## Auto-detected next action

MD

if [[ "${blocked_reason}" != "none" ]]; then
  printf '%s\n' "- Blocked. Run: /contract" >> "${STATUS_FILE}"
else
  printf '%s\n' "- Continue with: /build" >> "${STATUS_FILE}"
fi

printf '%s\n' "Wrote ${STATUS_FILE}"
printf '%s\n' "Wrote ${ORCH_FILE}"

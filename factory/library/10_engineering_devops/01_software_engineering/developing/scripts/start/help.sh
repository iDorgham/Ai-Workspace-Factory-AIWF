#!/usr/bin/env bash
# Plain-language index of everything you can do before and after /init.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

printf '\n'
printf '%s\n' "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf '%s\n' "  Sovereign Workspace"
printf '%s\n' "  Repo: ${ROOT}"
printf '%s\n' "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf '\n'

printf '%s\n' "▶ First time here? Run these in order:"
printf '%s\n' "  bash scripts/start/doctor.sh    Check that git and node are installed"
printf '%s\n' "  bash scripts/start/welcome.sh   Friendly checklist and next steps"
printf '%s\n' "  /init  (in your AI chat)        Set up your project — generates all project files"
printf '\n'

printf '%s\n' "▶ AI tool support (add or remove IDE / CLI integrations)"
printf '%s\n' "  bash scripts/tools/list-tools.sh                 See what is active"
printf '%s\n' "  bash scripts/tools/enable-ai-tools.sh --all    Enable every optional tool"
printf '%s\n' "  bash scripts/tools/enable-ai-tools.sh <a> <b>    Enable several by name"
printf '%s\n' "  bash scripts/tools/add-tool.sh <name>           Activate one tool"
printf '%s\n' "  bash scripts/tools/remove-tool.sh <name>       Deactivate a tool"
printf '%s\n' "  Available: codex  vscode  github  windsurf  gemini  qwen"
printf '%s\n' "             opencode  kilocode  copilot  amazonq  continue"
printf '\n'

printf '%s\n' "▶ Code quality (available after /init generates package.json)"
printf '%s\n' "  bash scripts/check/quick-check.sh    Fast lint/typecheck — no install"
printf '%s\n' "  bash scripts/check/full-check.sh     Install + full quality pipeline"
printf '\n'

printf '%s\n' "▶ Git shortcuts (available after /init)"
printf '%s\n' "  bash scripts/git/new-feature.sh <name>    Start a new feature branch"
printf '%s\n' "  bash scripts/git/get-updates.sh           Sync latest from main branch"
printf '%s\n' "  bash scripts/git/install-auto-checks.sh   Turn on auto checks on commit/push"
printf '\n'

printf '%s\n' "▶ AI workflow commands (type these in your AI chat)"
printf '%s\n' "  /init       Set up your project — START HERE"
printf '%s\n' "  /plan       Plan a new feature"
printf '%s\n' "  /contract   Create or lock a data contract (Zod schema)"
printf '%s\n' "  /build      Build a feature, component, or API"
printf '%s\n' "  /test       Run tests"
printf '%s\n' "  /quality    Run all quality gates"
printf '%s\n' "  /deploy     Deploy to preview or production"
printf '%s\n' "  /help       Get guidance from your AI team"
printf '\n'

printf '%s\n' "▶ Read more"
printf '%s\n' "  README.md                              Full guide with examples"
printf '%s\n' "  docs/workspace/guides/ONBOARDING.md   Step-by-step onboarding"
printf '%s\n' "  .ai/support/README.md                  Tool support catalog"
printf '%s\n' "  scripts/SCRIPTS_MAP.md                 Full script inventory"
printf '\n'

#!/usr/bin/env bash
# Start working on something new — creates a dedicated space for your changes.
# Usage: bash scripts/git/new-feature.sh my-feature-name
# Example: bash scripts/git/new-feature.sh user-login  →  creates: feature/user-login
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

slug="${1:-}"
if [[ -z "$slug" ]]; then
  printf '\n'
  printf '%s\n' "What do you want to build? Give it a short name (lowercase, hyphens only)."
  printf '\n'
  printf '%s\n' "Usage:   bash scripts/git/new-feature.sh <feature-name>"
  printf '%s\n' "Example: bash scripts/git/new-feature.sh user-login"
  printf '%s\n' "Example: bash scripts/git/new-feature.sh booking-page"
  printf '\n'
  exit 1
fi

if [[ ! "$slug" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  printf '%s\n' "Name must be lowercase with hyphens only (e.g. user-login, booking-page)."
  printf '%s\n' "No spaces, no capital letters, no special characters."
  exit 1
fi

if ! command -v git >/dev/null 2>&1; then
  printf '%s\n' "git is not installed. Install it from: https://git-scm.com"
  exit 1
fi

if ! git rev-parse --git-dir >/dev/null 2>&1; then
  printf '%s\n' "This folder is not a git repository yet. Run: git init"
  exit 1
fi

if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
  printf '%s\n' "You have unsaved changes. Save your work first (commit or stash), then try again."
  exit 1
fi

branch="feature/${slug}"
if git show-ref --verify --quiet "refs/heads/${branch}"; then
  printf '%s\n' "A branch called '${branch}' already exists. Choose a different name."
  exit 1
fi

git checkout -b "$branch"
printf '\n'
printf '%s\n' "Ready! You are now working on: ${branch}"
printf '%s\n' "When you're done, run /commit in your AI chat to save your work."
printf '\n'

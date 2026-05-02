#!/usr/bin/env bash
# Download the latest changes from your team — keeps your code up to date.
# Run this before starting new work to avoid conflicts.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

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

default_branch=""
if git rev-parse --verify refs/remotes/origin/HEAD >/dev/null 2>&1; then
  default_branch=$(git symbolic-ref -q refs/remotes/origin/HEAD | sed 's@^refs/remotes/origin/@@')
elif git show-ref --verify --quiet refs/heads/main; then
  default_branch=main
elif git show-ref --verify --quiet refs/heads/master; then
  default_branch=master
else
  printf '%s\n' "Could not find your main branch. Make sure you have connected to a remote (e.g. GitHub)."
  exit 1
fi

printf '→ Downloading latest changes...\n'
git fetch origin
printf '→ Switching to main branch (%s)...\n' "$default_branch"
git checkout "$default_branch"
printf '→ Applying updates...\n'
git pull --ff-only origin "$default_branch"
printf '\n'
printf '%s\n' "Done! Your code is up to date with: ${default_branch}"
printf '\n'

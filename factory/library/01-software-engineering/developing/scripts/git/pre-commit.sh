#!/usr/bin/env bash
# Sovereign optional hook entry (runtime pre-flight lives in scripts/hooks/run-pre-commit.sh).
# Symlink from .git/hooks/pre-commit → scripts/git/pre-commit if you want this path as hook.
# Skip: SKIP=1 or GALERIA_NO_HOOKS=1 git commit
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[[ -n "$ROOT" ]] || exit 0
exec bash "$ROOT/scripts/hooks/run-pre-commit.sh"

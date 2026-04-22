#!/usr/bin/env bash
# Point Cursor's agent-transcripts folder for this repo at .cursor/agent-transcripts/
# inside the workspace, so transcript files live under the project tree (not only under ~/.cursor).
#
# Prerequisite: open this repository in Cursor at least once so ~/.cursor/projects/<slug>/ exists.
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"

CURSOR_HOME="${CURSOR_HOME:-$HOME/.cursor}"
# Cursor names project dirs: absolute path without leading slash, '/' → '-'
slug="${ROOT#/}"
slug="${slug//\//-}"
PROJECT_DIR="${CURSOR_HOME}/projects/${slug}"
LOCAL_TRANSCRIPTS="${ROOT}/.cursor/agent-transcripts"
LINK_PATH="${PROJECT_DIR}/agent-transcripts"

if [[ ! -d "$CURSOR_HOME" ]]; then
  printf '%s\n' "Expected Cursor data at ${CURSOR_HOME} — install Cursor and open this repo once, then retry."
  exit 1
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
  printf '%s\n' "No Cursor project folder yet: ${PROJECT_DIR}"
  printf '%s\n' "Open this folder in Cursor (File → Open Folder → ${ROOT}), wait for indexing, then run:"
  printf '%s\n' "  bash scripts/cursor/symlink-agent-transcripts-to-workspace.sh"
  exit 1
fi

mkdir -p "$LOCAL_TRANSCRIPTS"

if [[ -e "$LINK_PATH" && ! -L "$LINK_PATH" ]]; then
  printf '%s\n' "→ Moving existing transcripts into workspace..."
  if command -v rsync >/dev/null 2>&1; then
    rsync -a "${LINK_PATH}/" "${LOCAL_TRANSCRIPTS}/"
  else
    cp -R "${LINK_PATH}/." "${LOCAL_TRANSCRIPTS}/" 2>/dev/null || true
  fi
  rm -rf "$LINK_PATH"
fi

ln -sfn "$LOCAL_TRANSCRIPTS" "$LINK_PATH"
printf '%s\n' "→ Symlink OK"
printf '    %s  →  %s\n' "$LINK_PATH" "$LOCAL_TRANSCRIPTS"
printf '%s\n' ""
printf '%s\n' "Agent transcript files are now stored under your repo at:"
printf '  %s\n' "$LOCAL_TRANSCRIPTS"
printf '%s\n' ""
printf '%s\n' "Paths under ~/.cursor/projects/.../agent-transcripts/ still appear in indexes; they resolve into the workspace via this symlink."
printf '%s\n' "Run /init (or scripts/git/init-gitignore.sh) so .gitignore ignores .cursor/agent-transcripts/."

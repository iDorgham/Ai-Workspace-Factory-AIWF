#!/usr/bin/env bash
# Write root .gitignore — run from /init Step 4 (bare template ships without .gitignore).
set -euo pipefail

_GALERIA_HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib/common.sh
source "${_GALERIA_HERE}/../lib/common.sh"
ROOT="$(sovereign_repo_root "${_GALERIA_HERE}")"
cd "$ROOT"

if [[ -f .gitignore ]] && [[ "${1:-}" != "--force" ]]; then
  printf '%s\n' ".gitignore already exists. Pass --force to replace with Sovereign defaults."
  exit 1
fi

cat >.gitignore <<'EOF'
# —— Sovereign /init — baseline ignore rules (edit after scaffold as needed)

# Dependencies
node_modules/
.pnp
.pnp.js

# Environment & secrets
.env
.env.*.local
!.env.example

# Build & caches
dist/
build/
out/
.next/
.turbo/
.cache/
*.tsbuildinfo

# Test & coverage
coverage/
.nyc_output/

# Logs & debug
*.log
npm-debug.log*
pnpm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db

# Cursor — local chat transcript bodies (optional symlink target)
.cursor/agent-transcripts/

# Vercel / deploy tooling (when used)
.vercel/

# Prisma
prisma/*.db
prisma/*.db-journal

# Misc
*.pem
.idea/
*.swp
*.swo
EOF

printf '%s\n' "→ Wrote ${ROOT}/.gitignore (Sovereign baseline; customize for your stack)"

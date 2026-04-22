#!/usr/bin/env bash
set -euo pipefail

FACTORY_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
log(){ printf "[factory] %s
" "$*"; }
now_iso(){ date -u +"%Y-%m-%dT%H:%M:%SZ"; }

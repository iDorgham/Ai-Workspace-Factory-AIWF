#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib/common.sh"
"$(dirname "$0")/rebuild-library-index.sh"
"$(dirname "$0")/validate-library.sh"
log "Library validation complete (indexes + metadata)"

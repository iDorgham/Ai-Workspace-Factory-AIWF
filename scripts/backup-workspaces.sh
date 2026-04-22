#!/bin/bash

# AIWF Workspace Backup Script
# Creates a timestamped archive of workspaces, .ai memory, and factory configuration.

set -e

BACKUP_DIR=".backup"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
FILENAME="aiwf_backup_${TIMESTAMP}.tar.gz"
FULL_PATH="${BACKUP_DIR}/${FILENAME}"

echo "🚀 Starting AIWF Workspace Backup..."

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Critical directories to backup
DIRS_TO_BACKUP="workspaces .ai factory master"

# Create compressed archive
echo "📦 Archiving directories: $DIRS_TO_BACKUP"
tar -czf "$FULL_PATH" $DIRS_TO_BACKUP

# Generate SHA256 checksum
echo "🔐 Generating checksum..."
if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "$FULL_PATH" > "${FULL_PATH}.sha256"
elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$FULL_PATH" > "${FULL_PATH}.sha256"
fi

echo "✅ Backup completed successfully!"
echo "📍 Location: $FULL_PATH"
echo "📜 Checksum: $(cat ${FULL_PATH}.sha256 | awk '{print $1}')"

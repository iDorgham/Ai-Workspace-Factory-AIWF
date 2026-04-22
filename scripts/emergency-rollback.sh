#!/bin/bash

# AIWF Emergency Rollback Script
# Automates the reversion to a stable v5 state.

set -e

BACKUP_DIR=".backup"
CONFIG_PATH="factory/registry/factory-config.json"

echo "🚨 EMERGENCY ROLLBACK INITIATED"

# Function to revert config
revert_config() {
    echo "⚙️ Reverting factory-config.json to v5 deterministic mode..."
    if [ -f "$CONFIG_PATH" ]; then
        # Simple sed replacement for demonstration; a more robust approach would use jq
        sed -i '' 's/"version": "6.0.0-alpha"/"version": "1.2.0"/g' "$CONFIG_PATH"
        sed -i '' 's/"swarm_routing": "v3"/"swarm_routing": "disabled"/g' "$CONFIG_PATH"
        echo "✅ Config reverted."
    else
        echo "❌ Error: factory-config.json not found."
        exit 1
    fi
}

# Function to list backups
list_backups() {
    echo "📦 Available Backups in $BACKUP_DIR:"
    if [ -d "$BACKUP_DIR" ]; then
        ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null || echo "No backups found."
    else
        echo "No backup directory found."
    fi
}

# Execution
echo "---"
revert_config
echo "---"
list_backups
echo "---"

echo "💡 To restore a specific backup, run:"
echo "   tar -xzf .backup/aiwf_backup_<timestamp>.tar.gz"
echo ""
echo "💡 To revert git state (if tag exists):"
echo "   git reset --hard v6.0.0-pre-migration"
echo ""
echo "🚨 Rollback automation complete. Please verify system state manually."

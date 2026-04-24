#!/bin/bash
# Pre-commit hook to prevent unauthorized JSON registry drift

echo "Running Pre-commit Schema validation..."

source factory/.env

# Basic validation script
python3 .ai/scripts/sync_registry.py > /dev/null

if ! git diff --exit-code .ai/registry/ > /dev/null; then
    echo "ERROR: Authorized registry schema drift detected!"
    echo "Please ensure you are not modifying .registry.json directly."
    exit 1
fi

echo "Schema validation passed. Version: $SCHEMA_VERSION"
exit 0

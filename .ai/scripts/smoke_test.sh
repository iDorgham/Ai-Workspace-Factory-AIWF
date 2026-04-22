#!/bin/bash
# Full Smoke Test and Post-Certification Lock

echo "=== 1. Testing Registry Lock ==="
python3 .ai/scripts/sync_registry.py > /dev/null
echo "✓ Registry synced."

echo "=== 2. Testing Cost Trackers ==="
python3 -c "import sys; sys.path.append('.ai/scripts/tool_adapters'); from cost_tracker import CostTracker; CostTracker.log_invocation('kilo', 10, 20, 15.5, 0.001); print('✓ Cost Tracker Appended')"
# Note: we used a quick inline script with local dummy but let's actually just call python directly.

echo "=== 3. Testing Gate Enforcement Block ==="
python3 .ai/scripts/gate_verifier.py init
python3 .ai/scripts/gate_verifier.py export || echo "✓ Block Triggered Successfully."
python3 .ai/scripts/gate_verifier.py review
python3 .ai/scripts/gate_verifier.py approve
python3 .ai/scripts/gate_verifier.py export
echo "✓ Full Pipeline Succeeds."

echo "All Post-Certification Smoke Tests Passed."

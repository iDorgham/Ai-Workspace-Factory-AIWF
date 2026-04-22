#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTORY_ROOT = ROOT.parent

def run_test(name, command):
    print(f"🧪 Running Test: {name}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(f"✅ PASSED: {name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED: {name}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    tests = [
        ("Structure Audit", f'python3 "{ROOT}/scripts/audit_path_integrity.py"'),
        ("Master Memory Sync", f'python3 "{ROOT}/scripts/sync_master_memory.py"'),
        ("Root Dashboard Render", f'python3 "{ROOT}/scripts/render_dashboard.py" root "{ROOT}/dashboard"'),
        ("Sovereign Alias Resolution", f'python3 "{FACTORY_ROOT}/factory/scripts/compose.py" test-routing --pipeline sovereign --explain-routing'),
        ("Proactive Brainstorm Trigger", f'python3 "{ROOT}/scripts/proactive_brainstorm_trigger.py"'),
        ("Sovereign Assembly & Multi-IDE Mirroring", 'TIMESTAMP=$(date +%s) && SLUG="smoke_test_${TIMESTAMP}" && python3 "' + str(FACTORY_ROOT) + '/factory/scripts/compose.py" $SLUG --pipeline sovereign --verbose && [ -d "workspaces/${SLUG}/001_${SLUG}/.ai/agents" ] && [ -f "workspaces/${SLUG}/001_${SLUG}/.cursor/rules/command-routing.mdc" ] && [ -f "workspaces/${SLUG}/001_${SLUG}/.github/copilot-instructions.md" ]')
    ]

    passed = 0
    for name, cmd in tests:
        if run_test(name, cmd):
            passed += 1

    print(f"\n📊 Smoke Test Results: {passed}/{len(tests)} PASS")
    sys.exit(0 if passed == len(tests) else 1)

if __name__ == "__main__":
    main()

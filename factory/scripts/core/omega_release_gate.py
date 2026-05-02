#!/usr/bin/env python3
import os
import sys
import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

class OmegaReleaseGate:
    def __init__(self):
        self.results = {}
        self.points = [
            "path_integrity", "mirror_drift_0", "all_phases_not_draft",
            "no_tombstoned_imports", "law151_certified", "health_score_95",
            "test_coverage_80", "spec_density_5", "lint_clean",
            "security_scan_pass", "dependency_audit_pass", "governance_hash_match"
        ]
        self.script_checks = {
            "path_integrity": ("factory/library/scripts/maintenance/audit_path_integrity.py", []),
            "mirror_drift_0": ("factory/scripts/core/check_mirror_drift.py", ["--threshold", "0"]),
            "law151_certified": ("factory/library/scripts/maintenance/healing.py", []),
            "health_score_95": ("factory/scripts/maintenance/health_scorer.py", ["--min-score", "95"]),
            "spec_density_5": ("factory/scripts/core/spec_density_gate_v2.py", []),
        }

    def check_all(self):
        print("🏛️  [OMEGA GATE] Initializing 12-point release audit...")
        
        for point in self.points:
            check = self.script_checks.get(point)
            if not check:
                print(f"No configured audit for {point}. Failing closed.")
                self.results[point] = False
                continue
            script_path, args = check
            self.results[point] = self._run_audit(script_path, args)

        print("\n📝 Gate Status Details:")
        for point in self.points:
            status = "✅ PASS" if self.results.get(point) else "❌ FAIL"
            print(f"  - {point: <25}: {status}")

        score = sum(1 for v in self.results.values() if v)
        print(f"\n📊 Audit Score: {score}/12")
        
        if score == 12:
            print("✅ OMEGA GATE PASSED. Release certified.")
            return True
        else:
            print("❌ OMEGA GATE FAILED. Blocked by non-compliance.")
            return False

    def _run_audit(self, script_path, args=None):
        if args is None:
            args = []
        full_path = REPO_ROOT / script_path
        if not full_path.exists():
            print(f"Missing audit script: {script_path}")
            return False
        try:
            subprocess.check_call(["python3", str(full_path)] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

if __name__ == "__main__":
    gate = OmegaReleaseGate()
    if not gate.check_all():
        sys.exit(1)
    sys.exit(0)

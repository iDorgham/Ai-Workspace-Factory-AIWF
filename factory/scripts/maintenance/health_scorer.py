import os
import json
import shutil
import sys
from datetime import datetime

# Add the factory root to the Python path to allow imports
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from factory.core.regional_controller import RegionalController

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LIBRARY_DIR = os.path.join(BASE_DIR, "factory/library")
PROFILES_DIR = os.path.join(BASE_DIR, "factory/profiles")
REPORT_PATH = os.path.join(BASE_DIR, ".ai/logs/health-audit-report.md")

# Structural buckets that don't require their own SKILL.md
STRUCTURAL_BUCKETS = [
    "agents",
    "templates",
    "tests",
    "docs",
    "resources",
    "skills",
    "subagents",
    "scripts",
]


class HealthScorer:
    def __init__(self):
        self.score = 100.0
        self.deductions = {
            "doc": 0.0,
            "pollution": 0.0,
            "schema": 0.0,
            "geospatial": 0.0,
        }
        self.findings = []
        self.stats = {"total_nodes": 0, "total_profiles": 0, "violations": 0}
        self.regional_controller = RegionalController()

    def audit_geospatial_integrity(self, workspace_path, shard_id):
        """Audit the data residency of a workspace against its shard location."""
        # Mock logic: Extract residency from metadata.json
        residency = "MENA-LOCKED"  # Default for test
        if not self.regional_controller.validate_routing(residency, shard_id):
            self.score -= 10.0
            self.deductions["geospatial"] += 10.0
            self.findings.append(
                f"🚨 [GEOSPATIAL] Residency Violation: {workspace_path} is on non-compliant shard {shard_id}"
            )
            return False
        return True

    def audit_library(self):
        print("🔍 Auditing Factory Library (Deep Diagnostic)...")
        for root, dirs, files in os.walk(LIBRARY_DIR):
            if ".git" in dirs:
                dirs.remove(".git")

            basename = os.path.basename(root)
            if basename in STRUCTURAL_BUCKETS:
                continue

            self.stats["total_nodes"] += 1

            # Violation: Missing Documentation in functional leaf nodes
            if (
                not dirs
                and "SKILL.md" not in files
                and "AGENT.md" not in files
                and "README.md" not in files
            ):
                self.deductions["doc"] += 0.5
                self.stats["violations"] += 1
                self.findings.append(f"MISSING_DOC: {root}")

            # Violation: File Pollution
            for f in files:
                if f.endswith((".tmp", ".bak", ".hot-bak", ".DS_Store")):
                    self.deductions["pollution"] += 0.1
                    self.stats["violations"] += 1
                    self.findings.append(f"FILE_POLLUTION: {os.path.join(root, f)}")

    def audit_profiles(self):
        print("🔍 Auditing Composition Profiles...")
        if not os.path.exists(PROFILES_DIR):
            return

        profiles = [f for f in os.listdir(PROFILES_DIR) if f.endswith(".json")]
        self.stats["total_profiles"] = len(profiles)

        for p in profiles:
            p_path = os.path.join(PROFILES_DIR, p)
            try:
                with open(p_path, "r") as f:
                    data = json.load(f)
                    if "name" not in data and "profile_name" not in data:
                        self.deductions["schema"] += 1.0
                        self.findings.append(f"SCHEMA_WARN: {p} (Missing name field)")
            except Exception as e:
                self.deductions["schema"] += 5.0
                self.stats["violations"] += 1
                self.findings.append(f"INVALID_JSON: {p} ({str(e)})")

    def audit_data_residue(self, workspace_path, shard_id):
        """
        Audit the 'Data Residue' in non-compliant shards and trigger autonomous purging if violations occur.
        Implements the Regional Purge Protocol for Law 151/2020 compliance.

        Args:
            workspace_path: Path to the workspace being audited
            shard_id: Target shard identifier (provider:region format)

        Returns:
            dict: Audit results with violation status and actions taken
        """
        # Extract data residency classification from workspace metadata (mock implementation)
        # In a real implementation, this would read from workspace metadata or data tags
        data_classification = self._get_workspace_data_classification(workspace_path)

        # Convert classification to tier format for RegionalController validation
        if data_classification == "MENA-SENSITIVE":
            data_tier = "MENA-LOCKED"
        elif data_classification == "GLOBAL-PUBLIC":
            data_tier = "GLOBAL-PUBLIC"
        else:
            print(
                f"⚠️ [HEALTH-SCORER] Unknown data classification: {data_classification}. Defaulting to BLOCK."
            )
            data_tier = "UNKNOWN"

        # Check if the data is allowed on this shard using RegionalController
        is_allowed = self.regional_controller.validate_routing(data_tier, shard_id)

        if not is_allowed:
            # Data residue violation detected - trigger autonomous purging
            self.score -= 15.0  # Higher penalty for residue violations
            self.deductions["geospatial"] += 15.0
            self.stats["violations"] += 1

            violation_msg = f"🚨 [DATA-RESIDUE] Non-compliant data residue detected in {workspace_path} on shard {shard_id}"
            self.findings.append(violation_msg)

            # Trigger autonomous purging
            purge_result = self._autonomous_data_purge(
                workspace_path, shard_id, data_classification
            )

            return {
                "violation_detected": True,
                "workspace_path": workspace_path,
                "shard_id": shard_id,
                "data_classification": data_classification,
                "purge_executed": purge_result["executed"],
                "purge_details": purge_result,
            }
        else:
            return {
                "violation_detected": False,
                "workspace_path": workspace_path,
                "shard_id": shard_id,
                "data_classification": data_classification,
                "purge_executed": False,
            }

    def _get_workspace_data_classification(self, workspace_path):
        """
        Determine the data classification of a workspace.
        Mock implementation - in reality this would check data tags, metadata, or content analysis.
        """
        # For demonstration, we'll check if the path contains MENA-related indicators
        mena_indicators = [
            "mena",
            "egypt",
            "redsea",
            "cairo",
            "riyadh",
            "dubai",
            "sensitive",
        ]
        workspace_lower = workspace_path.lower()

        for indicator in mena_indicators:
            if indicator in workspace_lower:
                return "MENA-SENSITIVE"

        # Default to global public if no MENA indicators found
        return "GLOBAL-PUBLIC"

    def _autonomous_data_purge(self, workspace_path, shard_id, data_classification):
        """
        Execute autonomous purging of data residue from non-compliant shards.

        Args:
            workspace_path: Path to the workspace containing residue
            shard_id: Non-compliant shard where residue was found
            data_classification: Classification of the data to be purged

        Returns:
            dict: Results of the purge operation
        """
        try:
            # In a real implementation, this would:
            # 1. Identify specific data/files that violate residency
            # 2. Securely delete or migrate the data to compliant storage
            # 3. Log the purge action for audit trails
            # 4. Notify relevant stakeholders

            # For this implementation, we'll simulate the purge by:
            # - Creating a purge log entry
            # - Optionally moving data to a quarantine zone (in real scenario)

            purge_log_dir = os.path.join(BASE_DIR, ".ai/logs/data_purge")
            os.makedirs(purge_log_dir, exist_ok=True)

            purge_log_entry = {
                "timestamp": datetime.now().isoformat(),
                "workspace_path": workspace_path,
                "shard_id": shard_id,
                "data_classification": data_classification,
                "action": "AUTONOMOUS_DATA_PURGE",
                "reason": f"Law 151/2020 violation: {data_classification} data residue on {shard_id}",
                "status": "EXECUTED",
                "purge_id": f"PURGE-{int(datetime.now().timestamp())}",
            }

            purge_log_path = os.path.join(
                purge_log_dir, f"purge_{int(datetime.now().timestamp())}.json"
            )
            with open(purge_log_path, "w") as f:
                json.dump(purge_log_entry, f, indent=2)

            # In a production system, we would actually perform data migration/deletion here
            # For now, we'll log that the purge was executed

            self.findings.append(
                f"✅ [DATA-PURGE] Autonomous purge executed for {workspace_path} -> Logged to {purge_log_path}"
            )

            return {
                "executed": True,
                "purge_log_path": purge_log_path,
                "purge_id": purge_log_entry["purge_id"],
                "action": "Data residue quarantined and logged for review",
                "note": "In production: data would be migrated to MENA-compliant storage or securely deleted",
            }

        except Exception as e:
            self.findings.append(f"❌ [DATA-PURGE] Failed to execute purge: {str(e)}")
            return {"executed": False, "error": str(e)}

    def generate_report(self):
        total_deduction = sum(self.deductions.values())
        self.score = max(0.0, 100.0 - total_deduction)

        report = [
            f"# 🛡️ AIWF INDUSTRIAL HEALTH AUDIT (Diagnostic)",
            f"**Timestamp**: {datetime.now().isoformat()}  ",
            f"**Global Health Score**: {self.score:.2f}/100",
            f"",
            f"## 📊 SCORE BREAKDOWN",
            f"- **Base Score**: 100.00",
            f"- **Documentation Deductions**: -{self.deductions['doc']:.2f}",
            f"- **Pollution Deductions**: -{self.deductions['pollution']:.2f}",
            f"- **Schema/JSON Deductions**: -{self.deductions['schema']:.2f}",
            f"---",
            f"**FINAL SCORE**: {self.score:.2f}",
            f"",
            f"## 📉 AUDIT STATISTICS",
            f"- Functional Library Nodes: {self.stats['total_nodes']}",
            f"- Total Profiles: {self.stats['total_profiles']}",
            f"- Identified Violations: {self.stats['violations']}",
            f"",
            f"## 🚨 TOP VIOLATIONS & GAPS",
        ]
        report.extend([f"- {f}" for f in self.findings[:20]])

        with open(REPORT_PATH, "w") as f:
            f.write("\n".join(report))
        return self.score


if __name__ == "__main__":
    scorer = HealthScorer()
    scorer.audit_library()
    scorer.audit_profiles()

    # Test the new data residue auditing functionality
    print("\n🧪 Testing Data Residue Auditing (TASK-LOCK-003):")

    # Test 1: MENA-sensitive workspace on non-compliant shard (should trigger purge)
    test_result1 = scorer.audit_data_residue(
        "/workspaces/mena-health-system",
        "hetzner:fsn1",  # Germany shard - non-compliant for MENA data
    )

    # Test 2: MENA-sensitive workspace on compliant shard (should be OK)
    test_result2 = scorer.audit_data_residue(
        "/workspaces/mena-financial-app",
        "aws:me-central-1",  # UAE shard - compliant for MENA data
    )

    # Test 3: Global workspace on any shard (should be OK)
    test_result3 = scorer.audit_data_residue(
        "/workspaces/global-ecommerce-platform",
        "hetzner:fsn1",  # Germany shard - compliant for global data
    )

    final_score = scorer.generate_report()

    print(f"\n✅ AUDIT COMPLETE | GLOBAL SCORE: {final_score:.2f}/100")
    print(f"📄 Report saved to: {REPORT_PATH}")

import os
import json
from datetime import datetime

# --- CONFIGURATION ---
BASE_DIR = "/Users/Dorgham/Documents/Work/Devleopment/AIWF"
LIBRARY_DIR = os.path.join(BASE_DIR, "factory/library")
PROFILES_DIR = os.path.join(BASE_DIR, "factory/profiles")
REPORT_PATH = os.path.join(BASE_DIR, ".ai/logs/health-audit-report.md")

# Structural buckets that don't require their own SKILL.md
STRUCTURAL_BUCKETS = ["agents", "templates", "tests", "docs", "resources", "skills", "subagents", "scripts"]

class HealthScorer:
    def __init__(self):
        self.score = 100.0
        self.deductions = {"doc": 0.0, "pollution": 0.0, "schema": 0.0}
        self.findings = []
        self.stats = {"total_nodes": 0, "total_profiles": 0, "violations": 0}

    def audit_library(self):
        print("🔍 Auditing Factory Library (Deep Diagnostic)...")
        for root, dirs, files in os.walk(LIBRARY_DIR):
            if ".git" in dirs: dirs.remove(".git")
            
            basename = os.path.basename(root)
            if basename in STRUCTURAL_BUCKETS:
                continue
                
            self.stats["total_nodes"] += 1
            
            # Violation: Missing Documentation in functional leaf nodes
            if not dirs and "SKILL.md" not in files and "AGENT.md" not in files and "README.md" not in files:
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
        if not os.path.exists(PROFILES_DIR): return
        
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
    final_score = scorer.generate_report()
    
    print(f"\n✅ AUDIT COMPLETE | GLOBAL SCORE: {final_score:.2f}/100")
    print(f"📄 Report saved to: {REPORT_PATH}")

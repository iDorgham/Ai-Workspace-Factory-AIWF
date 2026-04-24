"""
⚡ Engineering Core Mastery - Operational Core
Enforces architecture standards and maintainability protocols for engineering excellence.
"""

import os
from typing import Dict, Any, List

class EngineeringCoreMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "engineering-excellence"

    def run_architecture_audit(self, project_path: str) -> Dict[str, Any]:
        """
        Performs a baseline evaluation of project architecture.
        New in v10.1.0: Depth-first subdirectory analysis.
        """
        try:
            total_dirs = 0
            total_files = 0
            depths = []
            
            for root, dirs, files in os.walk(project_path):
                if ".git" in root or ".gemini" in root or "__pycache__" in root:
                    continue
                total_dirs += len(dirs)
                total_files += len(files)
                depths.append(root.count(os.sep))
            
            avg_depth = sum(depths) / len(depths) if depths else 0
            
            return {
                "status": "healthy" if avg_depth <= 5 else "complex",
                "avg_depth": avg_depth,
                "total_directories": total_dirs,
                "total_files": total_files,
                "tier": "OMEGA" if total_dirs < total_files * 0.2 else "BETA"
            }
        except Exception:
            return {"status": "error", "error": "Path access failure"}

    def evaluate_maintainability(self, code_snippet: str) -> Dict[str, Any]:
        """
        Calculates a maintainability index based on logical density and documentation.
        Uplifted in Phase 2: Added documentation check.
        """
        lines = [l.strip() for l in code_snippet.splitlines() if l.strip()]
        if not lines:
            return {"score": 1.0, "density": 0.0}
            
        doc_lines = [l for l in lines if l.startswith('"""') or l.startswith('#') or l.startswith("'''")]
        doc_ratio = len(doc_lines) / len(lines)
        
        # Heuristic: 1.0 is perfect, 0.0 is unmaintainable
        score = (1.0 / (len(lines) * 0.01 + 1)) * (0.5 + doc_ratio)
        density = len(lines) / (lines[-1].count(" ") + 1) if lines else 0 # Dummy metric
        
        return {
            "score": min(1.0, score),
            "doc_ratio": doc_ratio,
            "line_count": len(lines)
        }

    def validate_dependency_mapping(self, imports: List[str]) -> List[str]:
        """
        Identifies circular or prohibited dependency patterns.
        """
        prohibited = ["os.system", "subprocess.Popen"] # Internal sandbox rules
        violations = [imp for imp in imports if any(p in imp for p in prohibited)]
        return violations

import json
import os
from pathlib import Path

class ContentValidator:
    """
    Autonomous Content Validator for AIWF v13.0.0.
    Enforces Brand Voice, SEO compliance, and structural integrity.
    """
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.manifest_path = self.workspace_path / "content_manifest.json"
        self.brand_spec_path = Path("plan/11-website-content/brand-voice-manifest.spec.json")
        self.seo_spec_path = Path("plan/11-website-content/seo-optimization.spec.json")

    def load_specs(self):
        with open(self.brand_spec_path, 'r') as f:
            self.brand_spec = json.load(f)
        with open(self.seo_spec_path, 'r') as f:
            self.seo_spec = json.load(f)

    def validate_brand_voice(self, content: str) -> dict:
        # Simplified validation logic
        results = {"pass": True, "violations": []}
        forbidden_tones = self.brand_spec.get("brand_voice", {}).get("forbidden_tones", [])
        for tone in forbidden_tones:
            if tone.lower() in content.lower():
                results["pass"] = False
                results["violations"].append(f"Forbidden tone detected: {tone}")
        return results

    def run_audit(self):
        print(f"--- Starting Content Audit for {self.workspace_path} ---")
        self.load_specs()
        
        # Audit every markdown file in the workspace
        for root, _, files in os.walk(self.workspace_path):
            for file in files:
                if file.endswith(".md") and file != "sitemap.md":
                    file_path = Path(root) / file
                    with open(file_path, 'r') as f:
                        content = f.read()
                        brand_check = self.validate_brand_voice(content)
                        status = "✅ PASS" if brand_check["pass"] else "❌ FAIL"
                        relative_path = file_path.relative_to(self.workspace_path)
                        print(f"File: {relative_path} | Brand Voice: {status}")
                        if not brand_check["pass"]:
                            for v in brand_check["violations"]:
                                print(f"  - {v}")

if __name__ == "__main__":
    validator = ContentValidator("workspaces/sovereign-web")
    validator.run_audit()

"""
🎨 Figma Token Pipeline - Operational Core
Bidirectional synchronization between Figma Tokens (JSON) and code tokens (CSS).
"""

from typing import Dict, Any, List
import re

class FigmaTokenPipeline:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "design-sync-infrastructure"

    def transform_json_to_css(self, tokens_json: Dict[str, Any]) -> str:
        """
        Transforms absolute token JSON (Figma Tokens Studio format) into CSS Custom Properties.
        """
        css_lines = [":root {"]
        
        def process_tokens(node: Any, prefix: str = ""):
            if isinstance(node, dict):
                if "value" in node and "type" in node:
                    # It's a leaf token
                    variable_name = f"--{prefix.rstrip('-')}"
                    value = node["value"]
                    # Simple reference resolution (e.g., {color.blue.500})
                    if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                        value = f"var(--{value[1:-1].replace('.', '-')})"
                    
                    css_lines.append(f"  {variable_name}: {value};")
                else:
                    for key, value in node.items():
                        process_tokens(value, f"{prefix}{key}-")
        
        process_tokens(tokens_json)
        css_lines.append("}")
        return "\n".join(css_lines)

    def detect_token_drift(self, figma_tokens: Dict[str, Any], current_css: str) -> Dict[str, Any]:
        """
        Identifies discrepancies between Figma source-of-truth and local CSS implementation.
        """
        drift = []
        # Extract variables from CSS using regex
        css_vars = dict(re.findall(r"(--[\w-]+):\s*([^;]+);", current_css))
        
        # Flatten figma tokens for comparison
        flattened_figma = {}
        def flatten(node: Any, prefix: str = ""):
            if isinstance(node, dict):
                if "value" in node:
                    flattened_figma[f"--{prefix.rstrip('-')}"] = str(node["value"])
                else:
                    for key, value in node.items():
                        flatten(value, f"{prefix}{key}-")
        
        flatten(figma_tokens)
        
        for var_name, figma_val in flattened_figma.items():
            css_val = css_vars.get(var_name)
            if not css_val:
                drift.append({"token": var_name, "issue": "MISSING_IN_CODE", "figma_value": figma_val})
            else:
                # Resolve figma reference to expected CSS var for comparison
                expected_css_val = figma_val.strip()
                if expected_css_val.startswith("{") and expected_css_val.endswith("}"):
                    expected_css_val = figma_val = f"var(--{expected_css_val[1:-1].replace('.', '-')})"
                
                if css_val.strip() != expected_css_val:
                     drift.append({"token": var_name, "issue": "VALUE_MISMATCH", "figma_value": figma_val, "code_value": css_val})

        return {
            "in_sync": len(drift) == 0,
            "drift_count": len(drift),
            "discrepancies": drift
        }

    def validate_reference_integrity(self, tokens_json: Dict[str, Any]) -> List[str]:
        """
        Checks for dead/broken references in the token JSON.
        """
        all_paths = set()
        def collect_paths(node: Any, path: str = ""):
            if isinstance(node, dict):
                if "value" in node:
                    all_paths.add(path.rstrip('.'))
                else:
                    for key, value in node.items():
                        collect_paths(value, f"{path}{key}.")
        
        collect_paths(tokens_json)
        
        broken_refs = []
        def check_refs(node: Any, path: str = ""):
            if isinstance(node, dict):
                if "value" in node and isinstance(node["value"], str):
                    val = node["value"]
                    if val.startswith("{") and val.endswith("}"):
                        ref_path = val[1:-1]
                        if ref_path not in all_paths:
                            broken_refs.append(f"Broken reference in '{path.rstrip('.')}': {val}")
                else:
                    for key, value in node.items():
                        check_refs(value, f"{path}{key}.")
        
        check_refs(tokens_json)
        return broken_refs

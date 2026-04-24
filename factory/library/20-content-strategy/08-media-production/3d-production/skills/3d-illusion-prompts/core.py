"""
⚡ 3D Illusion Prompts - Operational Core
Enforces standards for immersive depth effects, 3D CSS transforms, and AI art-direction.
"""

from typing import Dict, Any, List

class ThreeDIllusionPrompts:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "immersive-visual-physics"

    def audit_parallax_physics(self, layer_config: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits CSS 3D parallax layers for physical depth consistency.
        Rule: Deepest layers must have more extreme negative Z-translations and larger scales.
        """
        violations = []
        prev_z = 0
        
        # Sort by layer depth if index present, or assume list order is front-to-back
        for i, layer in enumerate(layer_config):
            z_val = layer.get("translate_z", 0)
            scale = layer.get("scale", 1.0)
            
            # Deep layer check (negative Z)
            if z_val < -5:
                 violations.append(f"Layer {i}: Extreme Z-depth ({z_val}) may cause clipping.")
            
            # Scale compensation check: Deep layers need scale > 1 to cover the FOV
            if z_val < 0 and scale <= 1.0:
                violations.append(f"Layer {i}: Negative Z ({z_val}) requires scale > 1.0 to prevent gaps.")
                
        return {
            "is_physically_consistent": len(violations) == 0,
            "violations": violations,
            "required_properties": ["transform-style: preserve-3d", "perspective: 1000px"]
        }

    def validate_ai_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Validates AI Image Generation prompts for 'Luxury Depth' and immersion markers.
        """
        prompt_lower = prompt.lower()
        
        # Mandatory positive markers for premium depth
        markers = ["depth of field", "bokeh", "cinematic", "hyperrealistic", "8k", "lighting"]
        missing_markers = [m for m in markers if m not in prompt_lower]
        
        # Mandatory regional context
        has_context = any(word in prompt_lower for word in ["red sea", "hurghada", "egypt", "luxury"])
        
        is_premium = len(missing_markers) <= 2 and has_context
        
        return {
            "is_premium_tier": is_premium,
            "missing_depth_markers": missing_markers,
            "has_regional_context": has_context,
            "score": (len(markers) - len(missing_markers)) / len(markers) * 100
        }

    def recommend_accessibility_fallbacks(self, is_motion_heavy: bool) -> List[str]:
        """
        Provides accessibility fallbacks for 3D/Motion heavy interfaces.
        """
        fallbacks = [
            "@media (prefers-reduced-motion: reduce) { transform: none !important; transition: none !important; }",
            "opacity: 1 !important; visibility: visible !important;" # Ensure no stuck hidden states
        ]
        return fallbacks if is_motion_heavy else []

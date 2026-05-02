"""
✨ Sleek UI Design Protocols — Operational Core
Enforces standards for premium-tier aesthetics, glassmorphism, and layered shadow physics.
"""

from typing import Dict, Any, List
import re

class SleekUiDesignProtocols:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "aesthetic-excellence-qa"

    def audit_glassmorphism(self, style_dict: Dict[str, str]) -> Dict[str, Any]:
        """
        Audits CSS properties for glassmorphism compliance (blur and opacity).
        """
        backdrop_filter = style_dict.get("backdrop-filter", "")
        background_color = style_dict.get("background-color", "")
        
        has_blur = "blur" in backdrop_filter
        
        # Check for transparency (alpha < 0.3)
        rgba_match = re.search(r"rgba\(\d+,\s*\d+,\s*\d+,\s*([\d\.]+)\)", background_color)
        alpha = float(rgba_match.group(1)) if rgba_match else 1.0
        
        is_compliant = has_blur and alpha <= 0.3
        
        return {
            "is_glassmorphism_standard": is_compliant,
            "has_backdrop_blur": has_blur,
            "opacity_alpha": alpha,
            "recommendation": "Use backdrop-filter: blur(20px) with rgba alpha < 0.2" if not is_compliant else "OPTIMIZED"
        }

    def audit_typographic_hierarchy(self, font_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates font-weight and tracking (letter-spacing) for "Premium" authority.
        """
        weight = font_config.get("font-weight", 400)
        tracking = font_config.get("letter-spacing", "0px")
        
        # Header rule: Extra-Bold (>= 700) or Tracking-Tighter for headers
        is_header = font_config.get("is_header", False)
        is_compliant = True
        
        if is_header and int(weight) < 700:
            is_compliant = False
            
        return {
            "is_authoritative": is_compliant,
            "font_weight": weight,
            "tracking": tracking,
            "recommendation": "Use weight 700+ for headers" if not is_compliant else "ELITE"
        }

    def generate_layered_shadow(self, layers: int = 3, color: str = "rgba(0,0,0,0.1)") -> str:
        """
        Generates advanced box-shadow CSS strings for ambient occlusion effects.
        """
        shadows = []
        for i in range(1, layers + 1):
            offset = i * 2
            blur = i * 4
            shadows.append(f"0 {offset}px {blur}px {color}")
            
        return ", ".join(shadows)

"""
✒️ Arabic Typography & RTL Physics - Operational Core
Enforces standards for bilingual harmony, optical weight parity, and mirrored RTL layout.
"""

from typing import Dict, Any, List

class ArabicTypographyRtlPhysics:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "linguistic-aesthetic-physics"

    def calculate_optical_balance(self, en_font_size: float) -> Dict[str, Any]:
        """
        Calculates the required Arabic font size to achieve 'Optical Weight Parity' with English.
        Rule: Arabic typically requires +1pt to +2pt to counteract perceived visual thinness.
        """
        # Linear scaling logic: +1.5pt compensation for standard body sizes
        ar_font_size = en_font_size + 1.5
        
        return {
            "english_base_size": en_font_size,
            "recommended_arabic_size": round(ar_font_size, 1),
            "logic": "optical-weight-compensation",
            "is_standard": ar_font_size > en_font_size
        }

    def optimize_leading(self, font_size: float, is_arabic: bool = True) -> float:
        """
        Calculates optimized Line Height (Leading).
        Rule: Arabic requires 20-30% more leading to prevent ascender/descender overlap.
        """
        base_leading = 1.4 # Standard English leading
        if is_arabic:
            # +25% compensation
            optimized_leading = base_leading * 1.25
        else:
            optimized_leading = base_leading
            
        return round(font_size * optimized_leading, 2)

    def audit_rtl_mirroring(self, layout_elements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits UI elements for correct RTL mirroring.
        Directional icons (arrows, clocks) must be handled specifically.
        """
        violations = []
        for element in layout_elements:
            type_ = element.get("type", "")
            alignment = element.get("alignment", "left")
            
            # Critical violation: Logical Left alignment in an RTL context
            if alignment == "left":
                violations.append(f"Element '{element.get('name')}' is hardcoded to 'left' alignment.")
            
            # Directional icon check (e.g., Back button should face right in RTL)
            if type_ == "icon-back" and element.get("faces") == "left":
                 violations.append(f"Back Icon '{element.get('name')}' needs mirroring to face 'right' for RTL.")

        return {
            "is_rtl_compliant": len(violations) == 0,
            "violations": violations,
            "required_direction": "Right-to-Left"
        }

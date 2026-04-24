"""
🎨 Visual Identity Design Mastery - Operational Core
Enforces the Physics of Design (8pt grid-snap, negative space breathing-room) and tool-consistency.
"""

from typing import Dict, Any, List

class VisualIdentityDesignMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "brand-identity-vanguards"

    def audit_negative_space(self, logo_dim: Dict[str, float], padding: float) -> Dict[str, Any]:
        """
        Audits if the "Clear Space" around a brand mark is equal to its primary character height (x-height).
        """
        x_height = logo_dim.get("x_height", 0)
        is_breathing = padding >= x_height
        
        return {
            "has_breathing_room": is_breathing,
            "x_height_ref": x_height,
            "actual_padding": padding,
            "is_standard": is_breathing
        }

    def validate_grid_snap(self, coordinates: List[Dict[str, float]], grid_size: int = 8) -> Dict[str, Any]:
        """
        Verifies if all anchor points and container edges are snapped to the 8pt or 4pt grid system.
        """
        violations = []
        for i, coord in enumerate(coordinates):
            x, y = coord.get("x", 0), coord.get("y", 0)
            if x % grid_size != 0 or y % grid_size != 0:
                violations.append(f"Point {i} at ({x}, {y}) is not snapped to {grid_size}pt grid.")
                
        return {
            "is_grid_compliant": len(violations) == 0,
            "grid_size": grid_size,
            "violations": violations,
            "compliance_percentage": (1 - len(violations) / len(coordinates)) * 100 if coordinates else 100
        }

    def verify_asset_format(self, asset_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enforces vector-first infrastructure for branding assets.
        """
        ext = asset_metadata.get("extension", "").lower()
        is_vector = ext in ["svg", "ai", "eps", "pdf"]
        
        return {
            "is_scalable_vector": is_vector,
            "extension": ext,
            "recommendation": "ALWAYS build core assets in Vector format for infinite scalability" if not is_vector else "INFRASTRUCTURE_APPROVED"
        }

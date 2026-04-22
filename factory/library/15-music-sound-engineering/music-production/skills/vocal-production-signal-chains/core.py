"""
🎤 Vocal Production & Signal Chains - Operational Core
Enforces serial processing standards, de-esser thresholds, and dynamic headroom auditing.
"""

from typing import Dict, Any, List

class VocalProductionSignalChains:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "acoustic-production-physics"

    def audit_signal_chain(self, current_chain: List[str]) -> Dict[str, Any]:
        """
        Validates the serial processing order of the vocal chain.
        Standard Order: PITCH -> CLEAN (EQ/De-ess) -> TONE (Sat/EQ) -> DYNAMICS (Comp).
        """
        standard_order = ["pitch", "clean", "tone", "dynamics"]
        normalized_chain = [s.lower() for s in current_chain]
        
        # Check if the sequence follows the logic (ignoring missing steps)
        # We check relative order of available steps
        violations = []
        found_indices = []
        for step in normalized_chain:
            if step in standard_order:
                found_indices.append(standard_order.index(step))
            else:
                violations.append(f"Unknown processing step: '{step}'")
        
        is_linear = found_indices == sorted(found_indices)
        if not is_linear:
            violations.append("NON-LINEAR CHAIN: Dynamics/Tone should follow Pitch/Clean to avoid magnifying artifacts.")
            
        return {
            "is_standard_chain": is_linear and not violations,
            "violations": violations,
            "recommended_order": standard_order
        }

    def calculate_de_esser_threshold(self, sibilance_peak_db: float, target_red_db: float = 3.0) -> Dict[str, Any]:
        """
        Calculates De-Esser threshold to targets sibilance (4kHz-8kHz) while preserving clarity.
        """
        # Threshold should usually be 3-6dB below the peak of the sibilance
        recommended_threshold = sibilance_peak_db - target_red_db
        
        return {
            "sibilance_peak": sibilance_peak_db,
            "recommended_threshold": round(recommended_threshold, 1),
            "target_reduction": target_red_db,
            "frequency_range": "4kHz - 8kHz"
        }

    def audit_dynamic_stages(self, compression_stages: List[float]) -> Dict[str, Any]:
        """
        Ensures multiple stages of subtle compression (3-5dB) are used instead of one heavy stage.
        """
        is_safe = True
        warnings = []
        
        for i, red in enumerate(compression_stages):
            if red > 6.0:
                is_safe = False
                warnings.append(f"Stage {i}: Excessive reduction ({red}dB). Vocal transparency risk.")
                
        if len(compression_stages) < 2 and any(r > 4.0 for r in compression_stages):
            warnings.append("Single-stage compression detected: Recommend serial compression (2x 3dB) for smoother results.")

        return {
            "is_transparent": is_safe,
            "warnings": warnings,
            "stages_count": len(compression_stages)
        }

    def audit_spatial_integrity(self, spatial_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Ensures spatial effects (Reverb/Delay) don't mudy the vocal.
        Rule: Always Low-cut reverb up to 500Hz.
        """
        reverb_low_cut = spatial_config.get("reverb_low_cut_hz", 0)
        has_phase_alignment = spatial_config.get("phase_aligned", True)
        
        is_clear = reverb_low_cut >= 450 and has_phase_alignment
        
        return {
            "is_spatial_clean": is_clear,
            "low_cut_frequency": reverb_low_cut,
            "phase_status": "ALIGNED" if has_phase_alignment else "PHASE_ISSUE",
            "recommendation": "Increase reverb low-cut to > 500Hz to prevent muddiness." if reverb_low_cut < 450 else "CLEAR"
        }

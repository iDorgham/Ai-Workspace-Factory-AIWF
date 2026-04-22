"""
🤖 LLMO Audit (Large Language Model Optimization) — Operational Core
Measures brand perception, citation probability, and entity strength across frontier LLMs.
"""

from typing import Dict, Any, List
import re

class LlmoAudit:
    def __init__(self):
        self.version = "10.2.0"
        self.logic = "llm-visibility-engineering"

    def calculate_health_score(self, audit_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates a weighted LLMO Health Score based on 2026 ranking factors.
        Weights: Entity (97), Citation (95), Density (94), Structure (93), Freshness (92), Trust (90), MENA (88).
        """
        weights = {
            "entity_recognition": 97,
            "citation_probability": 95,
            "information_density": 94,
            "structured_data": 93,
            "freshness": 92,
            "brand_trust": 90,
            "mena_signals": 88
        }
        
        total_weight = sum(weights.values())
        weighted_sum = sum(audit_metrics.get(k, 0.0) * weights[k] for k in weights)
        
        score = (weighted_sum / total_weight)
        
        return {
            "llmo_health_score": round(score, 2),
            "is_omega_tier": score >= 88.0,
            "factor_breakdown": {k: audit_metrics.get(k, 0.0) for k in weights},
            "status": "CITABLE" if score >= 80.0 else "INVISIBLE"
        }

    def predict_citation_probability(self, model_responses: List[Dict[str, Any]], brand_entity: str) -> Dict[str, Any]:
        """
        Measures probability of direct citation across frontier models.
        """
        results = {}
        total_p = 0.0
        
        for resp in model_responses:
            model = resp.get("model", "unknown")
            text = resp.get("text", "")
            
            # Citation indicators: direct mentions, link inclusion, numeric references
            mention = 1.0 if brand_entity.lower() in text.lower() else 0.0
            references = 1.0 if re.findall(r"\[\d+\]|\w+\.\w+", text) else 0.0
            
            # Model-specific weighting (simulated for audit)
            probability = (mention * 0.6) + (references * 0.4)
            results[model] = round(probability, 2)
            total_p += probability
            
        return {
            "model_specific_probs": results,
            "average_citation_likelihood": round(total_p / len(model_responses), 2) if model_responses else 0.0,
            "target_models": list(results.keys())
        }

    def validate_mena_entity_authority(self, content_signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validates regional trust signals (ADGM, DIFC, local directories).
        """
        signals = ["ADGM", "DIFC", "DLD", "KSA_COMMERCE", "UAE_GOV"]
        verified_count = sum(1 for s in signals if content_signals.get(s, False))
        
        has_bilingual_parity = content_signals.get("has_ar_en_parity", False)
        
        score = (verified_count / len(signals)) * 100
        if has_bilingual_parity: score += 20 # Parity bonus
        
        return {
            "regional_authority_score": min(100, score),
            "verified_signals": [s for s in signals if content_signals.get(s)],
            "has_bilingual_parity": has_bilingual_parity,
            "status": "REGIONAL_AUTHORITY" if score >= 80 else "GENERIC"
        }

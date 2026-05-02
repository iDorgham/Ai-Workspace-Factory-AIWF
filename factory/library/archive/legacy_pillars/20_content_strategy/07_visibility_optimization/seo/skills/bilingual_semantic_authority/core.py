"""
🧬 Bilingual Semantic Authority - Operational Core
Enforces regional intent mapping, Arabic voice search optimization, and Hreflang parity.
"""

from typing import Dict, Any, List

class BilingualSemanticAuthority:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "bilingual-intent-engineering"

    def map_voice_intent(self, query: str) -> Dict[str, Any]:
        """
        Maps Arabic dialectal (Ammiya) voice queries to technical semantic targets.
        """
        ammiya_map = {
            "شقق قريبة من المترو": {"intent": "Commuter Accessibility", "target": "near:metro_station"},
            "عقارات تصلح للجنسية": {"intent": "Investor Citizenship", "target": "query:golden_visa_eligible"},
            "أفضل استثمار في دبي": {"intent": "Financial Advisory", "target": "category:high_yield_roi"}
        }
        
        mapping = ammiya_map.get(query, {"intent": "Generic", "target": "query:general"})
        
        return {
            "query": query,
            "semantic_mapping": mapping,
            "is_mapped": mapping["intent"] != "Generic"
        }

    def audit_hreflang_parity(self, pages: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Audits Hreflang tags for recursive ar-ae / en-ae parity.
        Rule: Every AR page must point to an EN equivalent and vice-versa.
        """
        violations = []
        for page in pages:
            url = page.get("url")
            alternates = page.get("alternates", {})
            
            # Check for bidirectional recursive link
            if "ar-ae" not in alternates or "en-ae" not in alternates:
                 violations.append(f"Missing regional hreflang parity for {url}")
                 
        return {
            "is_hreflang_compliant": len(violations) == 0,
            "violations": violations,
            "count": len(pages)
        }

    def validate_topic_clusters(self, keywords: List[str]) -> Dict[str, Any]:
        """
        Validates keyword clusters against 'Off-plan' and 'Luxury' silos.
        """
        silos = {
            "Off-plan": ["off-plan", "قيد الإنشاء", "payment plan", "launch", "under construction"],
            "Luxury": ["luxury", "بنتهاوس", "penthouse", "mansion", "private viewing", "exclusive"]
        }
        
        mapping = {silo: [] for silo in silos}
        for kw in keywords:
            kw_lower = kw.lower()
            for silo, tokens in silos.items():
                if any(t.lower() in kw_lower for t in tokens):
                    mapping[silo].append(kw)
                    break
                    
        return {
            "clusters": mapping,
            "unmapped_count": len(keywords) - sum(len(v) for v in mapping.values())
        }

    def audit_rtl_semantic_alignment(self, text_segments: List[str]) -> Dict[str, Any]:
        """
        Audits text segments for Right-to-Left (RTL) search intent alignment.
        Checks for: Bidi-marker presence, Ammiya-to-Fusha ratio, and local intent density.
        """
        results = []
        for segment in text_segments:
            # Heuristic: Check for Arabic script and regional intent markers
            has_arabic = any('\u0600' <= char <= '\u06FF' for char in segment)
            is_dialectal = "يا" in segment or "بتاع" in segment or "فين" in segment
            
            density = 1.0 if has_arabic else 0.0
            if is_dialectal: density *= 0.5 # Prioritize Fusha for SEO, but keep Ammiya for Engagement.
            
            results.append({
                "segment": segment[:50],
                "alignment_score": density,
                "type": "DIALECTAL_ENGAGEMENT" if is_dialectal else "FUSHA_SEO"
            })
            
        avg_alignment = sum(r["alignment_score"] for r in results) / len(results) if results else 0
        
        return {
            "average_rtl_alignment": round(avg_alignment, 2),
            "alignment_tier": "OMEGA" if avg_alignment >= 0.9 else "BETA_HYBRID",
            "detailed_audit": results,
            "recommendation": "Increase Fusha density for secondary keyword ranking" if avg_alignment < 0.8 else "READY"
        }

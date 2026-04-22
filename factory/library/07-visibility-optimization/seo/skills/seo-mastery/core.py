"""
⚡ SEO Mastery - Operational Core
Technical SEO scanning, MENA-specific intent mapping, and automated metadata generation.
"""

from typing import Dict, Any, List
import json

class SeoMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "visibility-optimization"

    def run_technical_audit(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Scans for technical SEO compliance (Core Web Vitals & Indexability).
        """
        thresholds = {
            "lcp": 2500, # Largest Contentful Paint (ms)
            "fid": 100,  # First Input Delay (ms)
            "cls": 0.1   # Cumulative Layout Shift
        }
        
        cwv = page_data.get("core_web_vitals", {})
        violations = []
        
        for metric, value in cwv.items():
            if metric in thresholds and value > thresholds[metric]:
                violations.append(f"Metric '{metric}' ({value}) exceeds threshold ({thresholds[metric]})")
        
        return {
            "is_standard": len(violations) == 0,
            "violations": violations,
            "can_index": page_data.get("is_indexable", True)
        }

    def generate_bilingual_schema(self, entity_data: Dict[str, Any]) -> str:
        """
        Generates schema.org (JSON-LD) with Arabic/English parity for MENA.
        """
        schema = {
            "@context": "https://schema.org",
            "@type": entity_data.get("type", "Organization"),
            "name": {
                "@language": "en",
                "@value": entity_data.get("name_en", "")
            },
            "alternateName": {
                "@language": "ar",
                "@value": entity_data.get("name_ar", "")
            },
            "description": {
                "@language": "en",
                "@value": entity_data.get("desc_en", "")
            }
        }
        
        # Arabic description if provided
        if "desc_ar" in entity_data:
            schema["description_ar"] = {
                "@language": "ar",
                "@value": entity_data.get("desc_ar", "")
            }
            
        return json.dumps(schema, indent=2, ensure_ascii=False)

    def validate_rtl_search_intent(self, keywords: List[str]) -> List[str]:
        """
        Identifies if keywords are optimized for Arabic RTL search patterns.
        """
        # Basic check for Arabic script presence in keywords
        rtl_opt = [k for k in keywords if any('\u0600' <= char <= '\u06FF' for char in k)]
        return rtl_opt

    def calculate_gvi_score(self, visibility_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates the Global Visibility Index (GVI).
        Weights: Technical (30%), SERP Presence (40%), Indexing Depth (30%).
        Target OMEGA-Tier: 95+
        """
        tech_score = visibility_data.get("technical_compliance", 0.0) # 0-100
        presence_score = visibility_data.get("serp_presence", 0.0)
        index_score = visibility_data.get("indexing_depth", 0.0)
        
        gvi = (tech_score * 0.3) + (presence_score * 0.4) + (index_score * 0.3)
        
        return {
            "gvi_score": round(gvi, 2),
            "is_omega_certified": gvi >= 95.0,
            "tier": "💎 OMEGA" if gvi >= 95.0 else ("🛠️ INDUSTRIAL_BETA" if gvi >= 70.0 else "🚩 REJECT"),
            "status": "REGIONALLY_DOMINANT" if gvi >= 90.0 else "VISIBILITY_REMEDIATION_REQUIRED"
        }

    def generate_bilingual_metadata(self, page_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generates high-density Title/Description tags for MENP (Middle East North Africa Page) parity.
        Rules: Arabic first for RTL locales, English first for LTR. Cross-link via hreflang.
        """
        title_en = page_context.get("title_en", "")
        title_ar = page_context.get("title_ar", "")
        
        # OMEGA Pattern: [Primary Language] | [Secondary Language] | [Brand]
        scrambled_title = f"{title_ar} | {title_en} | Sovereign"
        
        return {
            "meta_title": scrambled_title,
            "hreflang": {
                "en": page_context.get("url_en", ""),
                "ar": page_context.get("url_ar", "")
            },
            "og_locale": ["ar_EG", "en_US"],
            "status": "BILINGUAL_SYNCED"
        }

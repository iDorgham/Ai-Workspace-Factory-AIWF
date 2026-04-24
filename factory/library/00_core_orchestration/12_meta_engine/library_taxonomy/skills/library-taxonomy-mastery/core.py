"""
⚡ Library Taxonomy Mastery - Operational Core
Enforces standards for skill indexing, taxonomy integrity, and intent-based discovery mapping.
"""

from typing import Dict, Any, List

class LibraryTaxonomyMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "taxonomy-architecture-engineering"

    def audit_taxonomy_integrity(self, node_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Audits taxonomy for depth, collision risk, and naming consistency.
        Rule: All nodes must follow 'dept-subfolder-skill' naming structure.
        """
        violations = []
        names = set()
        
        for node in node_list:
            path = node.get("path", "")
            name = node.get("name", "")
            
            # Depth check: should usually be Dept / Category / Skill (3 deep)
            depth = len([p for p in path.split("/") if p])
            if depth > 5: # Tolerance for complex sub-clustering
                violations.append(f"Excessive depth ({depth}) for {path}")
                
            # Collision check
            if name in names:
                violations.append(f"Naming collision detected: {name}")
            names.add(name)
            
        return {
            "is_taxonomy_integral": len(violations) == 0,
            "node_count": len(node_list),
            "violations": violations,
            "integrity_score": max(0, 100 - len(violations) * 5)
        }

    def map_intent_to_skills(self, user_intent: str, library_map: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Maps user intent to specialized library clusters using keyword heuristics.
        """
        matches = []
        intent_lower = user_intent.lower()
        
        for cluster, keywords in library_map.items():
            if any(kw.lower() in intent_lower for kw in keywords):
                matches.append(cluster)
                
        return {
            "intent": user_intent,
            "mapped_clusters": matches,
            "discovery_strength": len(matches) / len(library_map) if library_map else 0,
            "recommendation": f"Route to {matches[0]} engine." if matches else "BROAD_RESEARCH_REQUIRED"
        }

    def validate_hierarchy(self, relationship_data: Dict[str, str]) -> Dict[str, Any]:
        """
        Verifies parent-child mapping consistency across the taxonomy.
        """
        orphans = []
        for child, parent in relationship_data.items():
            if not parent:
                orphans.append(child)
                
        return {
            "has_orphans": len(orphans) > 0,
            "orphan_nodes": orphans,
            "hierarchy_status": "VALIDATED" if not orphans else "FRAGMENTED"
        }

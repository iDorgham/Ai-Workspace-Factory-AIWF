"""
📐 Vector Database Architecture - Operational Core
Enforces high-performance indexing, hybrid RAG retrieval (RRF), and chunk-overlap auditing.
"""

from typing import List, Dict, Any

class VectorDBMastery:
    def __init__(self):
        self.version = "10.1.0"
        self.logic = "rag-memory-optimization"

    def select_indexing_strategy(self, data_size_m: float, latency_requirement_ms: float) -> Dict[str, Any]:
        """
        Recommends indexing strategy (HNSW vs IVF-Flat) based on scale and latency targets.
        """
        # Rule: HNSW for low-latency (< 100ms) or small-med scale (< 5M vectors).
        if latency_requirement_ms < 100 or data_size_m < 5:
            strategy = "HNSW"
            details = "Hierarchical Navigable Small World - High memory, ultra-low latency."
        else:
            strategy = "IVF-Flat"
            details = "Inverted File Index - Lower memory footprint, higher recall precision for large scale."
            
        return {
            "recommended_strategy": strategy,
            "rationale": details,
            "quantization_required": data_size_m > 10
        }

    def audit_chunk_overlap(self, chunks: List[str], min_overlap_chars: int = 100) -> Dict[str, Any]:
        """
        Heuristically audits chunks for sufficient semantic overlap to prevent context loss.
        """
        if len(chunks) < 2:
            return {"is_overlap_sufficient": True, "overlap_avg": 0}
            
        overlaps = []
        for i in range(len(chunks) - 1):
            c1 = chunks[i]
            c2 = chunks[i+1]
            
            # Simple suffix-prefix overlap check
            found_overlap = 0
            # Check last 500 chars of c1 against first 500 of c2
            tail = c1[-500:]
            head = c2[:500]
            
            for length in range(500, 10, -1):
                if tail[-length:] == head[:length]:
                    found_overlap = length
                    break
            overlaps.append(found_overlap)
            
        avg_overlap = sum(overlaps) / len(overlaps)
        is_sufficient = avg_overlap >= min_overlap_chars
        
        return {
            "is_overlap_sufficient": is_sufficient,
            "average_overlap_chars": round(avg_overlap, 2),
            "status": "PASS" if is_sufficient else "FAIL_FRAGILE_CONTEXT",
            "recommendation": "Increase chunk overlap to ~200 chars for OMEGA standard." if not is_sufficient else "STABLE"
        }

    def calculate_rrf(self, semantic_results: List[str], keyword_results: List[str], k: int = 60) -> List[str]:
        """
        Implements Reciprocal Rank Fusion (RRF) to re-rank hybrid results.
        """
        scores = {}
        for rank, item in enumerate(semantic_results):
            scores[item] = scores.get(item, 0) + (1.0 / (k + rank + 1))
        for rank, item in enumerate(keyword_results):
            scores[item] = scores.get(item, 0) + (1.0 / (k + rank + 1))
        
        # Sort keys by score descending
        ranked = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return ranked

    def simulate_omega_hybrid_retrieval(self, query: str, mock_db: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Simulates the entire RAG retrieval loop using OMEGA standards.
        Includes Semantic search mock, Keyword search mock, and RRF re-ranking.
        """
        semantic = mock_db.get("semantic", [])
        keyword = mock_db.get("keyword", [])
        
        re_ranked = self.calculate_rrf(semantic, keyword)
        
        return {
            "query": query,
            "top_results": re_ranked[:5],
            "retrieval_method": "HYBRID_RRF",
            "is_omega_compliant": len(re_ranked) > 0
        }

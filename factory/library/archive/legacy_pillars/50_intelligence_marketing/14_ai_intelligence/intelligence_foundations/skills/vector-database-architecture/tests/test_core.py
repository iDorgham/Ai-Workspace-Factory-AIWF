import unittest
from ..core import VectorDBMastery

class TestVectorDBMastery(unittest.TestCase):
    def setUp(self):
        self.vdb = VectorDBMastery()

    def test_select_indexing_strategy_hnsw(self):
        result = self.vdb.select_indexing_strategy(data_size_m=1.0, latency_requirement_ms=50)
        self.assertEqual(result["recommended_strategy"], "HNSW")
        self.assertFalse(result["quantization_required"])

    def test_select_indexing_strategy_ivf(self):
        result = self.vdb.select_indexing_strategy(data_size_m=20.0, latency_requirement_ms=200)
        self.assertEqual(result["recommended_strategy"], "IVF-Flat")
        self.assertTrue(result["quantization_required"])

    def test_audit_chunk_overlap_pass(self):
        text1 = "This is the first chunk of data. It ends with OMEGA."
        text2 = "It ends with OMEGA. This is the second chunk."
        result = self.vdb.audit_chunk_overlap([text1, text2], min_overlap_chars=10)
        self.assertTrue(result["is_overlap_sufficient"])
        self.assertGreater(result["average_overlap_chars"], 0)

    def test_audit_chunk_overlap_fail(self):
        text1 = "Completely different content here."
        text2 = "No overlap found at all in this sequence."
        result = self.vdb.audit_chunk_overlap([text1, text2], min_overlap_chars=10)
        self.assertFalse(result["is_overlap_sufficient"])

    def test_calculate_rrf(self):
        semantic = ["A", "B", "C"]
        keyword = ["C", "D", "A"]
        # C is in both, should be highly ranked
        result = self.vdb.calculate_rrf(semantic, keyword)
        self.assertEqual(result[0], "A") # Since A is 1st in sem, 3rd in key. C is 3rd/1st. 
        # Actually RRF(A) = 1/(60+1) + 1/(60+3). RRF(C) = 1/(60+3) + 1/(60+1). Same score.
        self.assertIn("A", result[:2])
        self.assertIn("C", result[:2])

    def test_simulate_omega_hybrid_retrieval(self):
        mock_db = {
            "semantic": ["Doc_A", "Doc_B"],
            "keyword": ["Doc_C", "Doc_A"]
        }
        result = self.vdb.simulate_omega_hybrid_retrieval("test query", mock_db)
        self.assertEqual(result["retrieval_method"], "HYBRID_RRF")
        self.assertIn("Doc_A", result["top_results"])
        self.assertTrue(result["is_omega_compliant"])

if __name__ == '__main__':
    unittest.main()

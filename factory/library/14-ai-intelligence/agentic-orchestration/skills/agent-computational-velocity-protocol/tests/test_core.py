import unittest
from ..core import VelocityProtocol

class TestVelocityProtocol(unittest.TestCase):
    def setUp(self):
        self.velocity = VelocityProtocol()

    def test_prune_context(self):
        files = ["a.py", "b.py", "c.py", "d.py"]
        pruned = self.velocity.prune_context(files)
        self.assertEqual(len(pruned), 3)
        self.assertEqual(pruned, ["a.py", "b.py", "c.py"])

    def test_inject_efficiency_system_rule(self):
        prompt = "Base prompt."
        result = self.velocity.inject_efficiency_system_rule(prompt)
        self.assertIn("CRITICAL SYSTEM RULE", result)

    def test_strip_conversational_padding(self):
        text = "Certainly! I will now do the task."
        result = self.velocity.strip_conversational_padding(text)
        self.assertNotIn("Certainly!", result)
        self.assertNotIn("I will now do", result)

    def test_track_latency(self):
        result = self.velocity.track_latency(start_time=10.0, end_time=11.5)
        self.assertEqual(result["latency_sec"], 1.5)
        self.assertEqual(result["performance_score"], 1.0)
        self.assertEqual(result["status"], "OMEGA_VELOCITY")

    def test_score_token_efficiency(self):
        # 100 tokens for 500 chars = 5.0 ratio (good)
        result = self.velocity.score_token_efficiency(token_count=100, information_chars=500)
        self.assertEqual(result["efficiency_ratio"], 5.0)
        self.assertTrue(result["is_token_optimized"])
        self.assertEqual(result["status"], "DENSE_INTELLIGENCE")

if __name__ == '__main__':
    unittest.main()

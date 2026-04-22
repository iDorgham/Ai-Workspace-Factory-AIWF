import unittest
from ..core import CommunityEngagementMastery

class TestCommunityEngagementMastery(unittest.TestCase):
    def setUp(self):
        self.comm = CommunityEngagementMastery()

    def test_audit_community_sentiment_healthy(self):
        feedback = [
            {"sentiment_score": 0.8},
            {"sentiment_score": 0.9},
            {"sentiment_score": 0.6},
            {"sentiment_score": 0.3}
        ]
        result = self.comm.audit_community_sentiment(feedback)
        self.assertGreater(result["sentiment_index"], 0.4)
        self.assertEqual(result["status"], "HEALTHY_ADVOCACY")

    def test_audit_community_sentiment_crisis(self):
        feedback = [
            {"sentiment_score": -0.8},
            {"sentiment_score": -0.9},
            {"sentiment_score": -0.5},
            {"sentiment_score": 0.8}
        ]
        result = self.comm.audit_community_sentiment(feedback)
        self.assertTrue(result["is_crisis_detected"])
        self.assertEqual(result["status"], "CRITICAL_SENTIMENT")

    def test_trigger_engagement_triage_high(self):
        crisis = {"is_crisis_detected": True}
        result = self.comm.trigger_engagement_triage(crisis)
        self.assertEqual(result["priority"], "HIGH")
        self.assertIn("MODERATOR_OVERRIDE", result["action"])

if __name__ == '__main__':
    unittest.main()

import unittest
from ..core import OpenAIOfficialMastery

class TestOpenAIOfficialMastery(unittest.TestCase):
    def setUp(self):
        self.openai = OpenAIOfficialMastery()

    def test_verify_sync_parity(self):
        active = ["official-chat-gpt", "official-o1"]
        result = self.openai.verify_sync_parity("official-o1", active)
        self.assertEqual(result["status"], "SYNCED")
        self.assertTrue(result["can_invoke"])

        result_fail = self.openai.verify_sync_parity("missing-skill", active)
        self.assertEqual(result_fail["status"], "PENDING_SYNC")
        self.assertFalse(result_fail["can_invoke"])

    def test_get_invocation_command(self):
        self.assertEqual(self.openai.get_invocation_command("official-o1-mastery"), "/o1")
        self.assertEqual(self.openai.get_invocation_command("official-chat-gpt"), "/chat-gpt")

    def test_audit_rate_limits(self):
        gpt4o = self.openai.audit_rate_limits("gpt-4o")
        self.assertEqual(gpt4o["rpm"], 10000)
        
        default = self.openai.audit_rate_limits("unknown-model")
        self.assertEqual(default["rpm"], 3500)

if __name__ == '__main__':
    unittest.main()

import unittest
import time
from ..core import ClaudeMastery

class TestClaudeMastery(unittest.TestCase):
    def setUp(self):
        self.claude = ClaudeMastery()

    def test_compress_prompt_enabled(self):
        prompt = "Sure thing! I'm happy to help, here is your code."
        compressed = self.claude.compress_prompt(prompt, enabled=True)
        self.assertNotIn("Sure thing!", compressed)
        self.assertNotIn("I'm happy to help,", compressed)

    def test_compress_prompt_disabled(self):
        prompt = "Sure thing! I'm happy to help, here is your code."
        compressed = self.claude.compress_prompt(prompt, enabled=False)
        self.assertEqual(prompt, compressed)

    def test_inject_thinking_protocol_needed(self):
        prompt = "Explain quantum physics."
        result = self.claude.inject_thinking_protocol(prompt)
        self.assertIn("<thinking>", result)

    def test_validate_prompt_structure_fail(self):
        prompt = "Just an instruction."
        result = self.claude.validate_prompt_structure(prompt)
        self.assertFalse(result["is_structured"])

if __name__ == '__main__':
    unittest.main()

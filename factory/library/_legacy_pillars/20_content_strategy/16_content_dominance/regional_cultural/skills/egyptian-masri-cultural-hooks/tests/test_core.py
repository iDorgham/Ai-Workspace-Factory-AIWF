import unittest
from ..core import EgyptianMasriCulturalHooks

class TestEgyptianMasriCulturalHooks(unittest.TestCase):
    def setUp(self):
        self.hooks = EgyptianMasriCulturalHooks()

    def test_apply_sarcasm_loop_injected(self):
        hook = "عايز تسكن في القاهرة؟"
        result = self.hooks.apply_sarcasm_loop(hook)
        self.assertTrue(result["sarcasm_injected"])
        self.assertIn("يليق بيك", result["modified_hook"])

    def test_dialect_scrambler_business(self):
        content = "محتاجين نخلص المشروع"
        result = self.hooks.dialect_scrambler(content, "BUSINESS")
        self.assertTrue(result["is_localized_cairene"])
        self.assertIn("يا باشا", result["content"])

    def test_map_emotional_resonance_trust(self):
        result = self.hooks.map_emotional_resonance("TRUST")
        self.assertIn("Generosity (Karam)", result["active_resonators"])

if __name__ == '__main__':
    unittest.main()

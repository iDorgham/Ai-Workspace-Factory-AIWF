import unittest
from ..core import FigmaTokenPipeline

class TestFigmaTokenPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = FigmaTokenPipeline()
        self.sample_tokens = {
            "global": {
                "color": {
                    "blue": {"500": {"value": "#3b82f6", "type": "color"}},
                    "primary": {"value": "{global.color.blue.500}", "type": "color"}
                }
            }
        }

    def test_transform_json_to_css(self):
        css = self.pipeline.transform_json_to_css(self.sample_tokens)
        self.assertIn("--global-color-blue-500: #3b82f6;", css)
        self.assertIn("--global-color-primary: var(--global-color-blue-500);", css)

    def test_detect_token_drift_no_drift(self):
        current_css = ":root { --global-color-blue-500: #3b82f6; --global-color-primary: var(--global-color-blue-500); }"
        result = self.pipeline.detect_token_drift(self.sample_tokens, current_css)
        self.assertTrue(result["in_sync"])

    def test_detect_token_drift_with_drift(self):
        current_css = ":root { --global-color-blue-500: #ff0000; }"
        result = self.pipeline.detect_token_drift(self.sample_tokens, current_css)
        self.assertFalse(result["in_sync"])
        self.assertEqual(result["drift_count"], 2) # Missing primary, value mismatch on blue-500

    def test_validate_reference_integrity_pass(self):
        broken = self.pipeline.validate_reference_integrity(self.sample_tokens)
        self.assertEqual(len(broken), 0)

    def test_validate_reference_integrity_fail(self):
        broken_tokens = {
            "primary": {"value": "{global.color.missing}", "type": "color"}
        }
        broken = self.pipeline.validate_reference_integrity(broken_tokens)
        self.assertEqual(len(broken), 1)
        self.assertIn("Broken reference", broken[0])

if __name__ == '__main__':
    unittest.main()

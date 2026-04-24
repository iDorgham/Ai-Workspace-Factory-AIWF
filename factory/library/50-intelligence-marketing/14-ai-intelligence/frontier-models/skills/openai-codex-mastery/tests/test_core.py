import unittest
from ..core import OpenAIMastery

class TestOpenAIMastery(unittest.TestCase):
    def setUp(self):
        self.openai = OpenAIMastery()

    def test_slice_context_window_mid(self):
        lines = [str(i) for i in range(2000)]
        # Target index 1000, should give [500:1500]
        result = self.openai.slice_context_window(lines, 1000)
        self.assertEqual(len(result), 1000)
        self.assertEqual(result[0], "500")
        self.assertEqual(result[-1], "1499")

    def test_validate_function_schema_pass(self):
        schema = {
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query to find relevant documents."}
                },
                "required": ["query"]
            }
        }
        result = self.openai.validate_function_schema(schema)
        self.assertTrue(result["is_schema_compliant"])
        self.assertEqual(result["status"], "PRODUCTION_READY")

    def test_validate_function_schema_fail_docs(self):
        schema = {
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "short"}
                },
                "required": ["query"]
            }
        }
        result = self.openai.validate_function_schema(schema)
        self.assertFalse(result["is_schema_compliant"])
        self.assertEqual(result["status"], "HALLUCINATION_RISK")

    def test_audit_token_economy_full(self):
        config = {
            "stop": ["\n"],
            "logit_bias": {"50256": -100},
            "response_format": {"type": "json_object"}
        }
        result = self.openai.audit_token_economy(config)
        self.assertEqual(result["economy_score"], 100)
        self.assertTrue(result["is_json_optimized"])

if __name__ == '__main__':
    unittest.main()

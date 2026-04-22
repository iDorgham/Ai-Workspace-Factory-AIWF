"""
Codex Tool Adapter

Integrates with an OpenAI-compatible endpoint for Codex-style code tasks.
"""

import os
import time

from .base_adapter import ToolAdapter

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class CodexAdapter(ToolAdapter):
    """Codex tool adapter for code-first execution and review."""

    INPUT_PRICE_PER_1K = 0.002
    OUTPUT_PRICE_PER_1K = 0.0004

    def __init__(self, api_key: str = None, config: dict = None):
        api_key = api_key or os.getenv("CODEX_API_KEY")
        config = config or {}
        super().__init__("codex", api_key, config)

        if OpenAI is None:
            raise ImportError("openai package required. Install: pip install openai")

        base_url = config.get("base_url", os.getenv("CODEX_BASE_URL"))
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = config.get("model", "codex")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 0.2)

    def execute(self, command: str, language: str = None, **kwargs) -> dict:
        start_time = time.time()

        try:
            prompt = command if not language else f"[Language: {language}]\n{command}"
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
            )

            output_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens
            cost = self.calculate_cost(input_tokens, output_tokens)
            latency = time.time() - start_time

            self.update_stats(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                success=True,
            )
            self.track_performance(latency, True)

            return {
                "status": "success",
                "output": output_text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "latency": latency,
                "model": self.model,
            }
        except Exception as error:
            latency = time.time() - start_time
            self.update_stats(success=False, error=str(error))
            self.track_performance(latency, False)
            return self.handle_error(error)

    def count_tokens(self, text: str, **kwargs) -> int:
        return len(text) // 5

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        input_cost = (input_tokens / 1000) * self.INPUT_PRICE_PER_1K
        output_cost = (output_tokens / 1000) * self.OUTPUT_PRICE_PER_1K
        return round(input_cost + output_cost, 6)

    def handle_error(self, error: Exception) -> dict:
        error_type = type(error).__name__
        error_message = str(error)
        lowered = error_message.lower()

        if "rate_limit" in lowered:
            recovery = "retry_with_backoff"
            user_message = "Codex rate limit reached. Retrying..."
        elif "authentication" in lowered or "401" in lowered:
            recovery = "fallback_to_next_tool"
            user_message = "Codex authentication failed. Switching to next tool."
        elif "timeout" in lowered:
            recovery = "retry_with_backoff"
            user_message = "Codex request timed out. Retrying..."
        else:
            recovery = "fallback_to_next_tool"
            user_message = "Codex request failed. Switching to next tool."

        return {
            "status": "error",
            "error": error_message,
            "error_type": error_type,
            "recovery": recovery,
            "user_message": user_message,
            "tool": "codex",
        }

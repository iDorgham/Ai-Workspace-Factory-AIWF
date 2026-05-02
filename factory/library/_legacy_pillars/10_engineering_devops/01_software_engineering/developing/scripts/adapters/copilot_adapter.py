"""
Copilot Tool Adapter

Integrates with Microsoft Copilot for code generation and review.
Specializes in code tasks, technical documentation.
"""

import time
import os
from .base_adapter import ToolAdapter

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class CopilotAdapter(ToolAdapter):
    """Copilot tool adapter for code generation and review"""

    # Pricing (April 2026)
    INPUT_PRICE_PER_1K = 0.002       # $0.002 per 1K tokens
    OUTPUT_PRICE_PER_1K = 0.006      # $0.006 per 1K tokens

    def __init__(self, api_key: str = None, config: dict = None):
        """Initialize Copilot adapter for code tasks."""
        api_key = api_key or os.getenv("COPILOT_API_KEY")
        config = config or {}
        super().__init__("copilot", api_key, config)

        if OpenAI is None:
            raise ImportError("openai package required. Install: pip install openai")

        # Initialize OpenAI-compatible client (Copilot uses OpenAI API)
        self.client = OpenAI(api_key=api_key)

        # Configuration
        self.model = config.get("model", "copilot")
        self.max_tokens = config.get("max_tokens", 2048)
        self.temperature = config.get("temperature", 0.7)

    def execute(self, command: str, language: str = None, **kwargs) -> dict:
        """Execute code task via Copilot API."""
        start_time = time.time()

        try:
            # Enhance prompt with language context
            prompt = command
            if language:
                prompt = f"[Language: {language}]\n{command}"

            # Call Copilot API (OpenAI-compatible)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            # Extract data
            output_text = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            # Calculate cost
            cost = self.calculate_cost(input_tokens, output_tokens)

            # Track latency
            latency = time.time() - start_time

            # Update statistics
            self.update_stats(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=cost,
                success=True
            )
            self.track_performance(latency, True)

            # Return success response
            return {
                "status": "success",
                "output": output_text,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost": cost,
                "latency": latency,
                "model": self.model
            }

        except Exception as e:
            latency = time.time() - start_time
            self.update_stats(success=False, error=str(e))
            self.track_performance(latency, False)
            return self.handle_error(e)

    def count_tokens(self, text: str, **kwargs) -> int:
        """Count tokens for code (usually shorter than text)."""
        # Approximation: code ~5 chars per token (due to punctuation)
        return len(text) // 5

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with Copilot pricing."""
        input_cost = (input_tokens / 1000) * self.INPUT_PRICE_PER_1K
        output_cost = (output_tokens / 1000) * self.OUTPUT_PRICE_PER_1K
        return round(input_cost + output_cost, 6)

    def handle_error(self, error: Exception) -> dict:
        """Handle Copilot-specific errors."""
        error_type = type(error).__name__
        error_message = str(error)

        # Classify error
        if "rate_limit" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Copilot rate limit reached. Retrying..."
        elif "context_length_exceeded" in error_message.lower() or "token" in error_message.lower():
            recovery = "fallback_to_next_tool"
            user_message = "Code too long for Copilot. Switching to next tool."
        elif "authentication" in error_message.lower() or "401" in error_message:
            recovery = "fallback_to_next_tool"
            user_message = "Copilot authentication failed. Switching to next tool."
        elif "timeout" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Copilot request timed out. Retrying..."
        else:
            recovery = "fallback_to_next_tool"
            user_message = f"Copilot error. Switching to next tool."

        return {
            "status": "error",
            "error": error_message,
            "error_type": error_type,
            "recovery": recovery,
            "user_message": user_message,
            "tool": "copilot"
        }

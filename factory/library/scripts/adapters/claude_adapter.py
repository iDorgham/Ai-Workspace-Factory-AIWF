"""
Claude Tool Adapter

Integrates with Anthropic's Claude API for text generation.
Specializes in long context, high-quality output.
"""

import time
import os
from .base_adapter import ToolAdapter

try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None


class ClaudeAdapter(ToolAdapter):
    """Claude tool adapter for Anthropic API integration"""

    # Pricing (April 2026)
    INPUT_PRICE_PER_1K = 0.003      # $0.003 per 1K input tokens
    OUTPUT_PRICE_PER_1K = 0.009     # $0.009 per 1K output tokens

    def __init__(self, api_key: str = None, config: dict = None):
        """
        Initialize Claude adapter.

        Args:
            api_key (str): Anthropic API key
            config (dict): Configuration options
        """
        api_key = api_key or os.getenv("CLAUDE_API_KEY")
        config = config or {}
        super().__init__("claude", api_key, config)

        if Anthropic is None:
            raise ImportError("anthropic package required. Install: pip install anthropic")

        # Initialize Anthropic client
        self.client = Anthropic(api_key=api_key)

        # Configuration
        self.model = config.get("model", "claude-opus-4-6")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 1.0)
        self.system_prompt = config.get("system_prompt", None)

    def execute(self, command: str, **kwargs) -> dict:
        """Execute a command via Claude API."""
        start_time = time.time()

        try:
            # Prepare messages
            messages = [{"role": "user", "content": command}]

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=self.system_prompt,
                messages=messages
            )

            # Extract data from response
            input_tokens = response.usage.input_tokens
            output_tokens = response.usage.output_tokens
            output_text = response.content[0].text

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
        """Count tokens in text."""
        # Approximation: ~4 characters per token
        return len(text) // 4

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage."""
        input_cost = (input_tokens / 1000) * self.INPUT_PRICE_PER_1K
        output_cost = (output_tokens / 1000) * self.OUTPUT_PRICE_PER_1K
        return round(input_cost + output_cost, 6)

    def handle_error(self, error: Exception) -> dict:
        """Handle Claude-specific errors."""
        error_type = type(error).__name__
        error_message = str(error)

        # Classify error and suggest recovery
        if "rate_limit" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Claude API rate limit exceeded. Retrying in fallback chain."
        elif "invalid_request" in error_message.lower():
            recovery = "fallback_to_next_tool"
            user_message = "Invalid request to Claude API. Switching to next tool."
        elif "authentication" in error_message.lower() or "401" in error_message:
            recovery = "fallback_to_next_tool"
            user_message = "Authentication failed with Claude API. Switching to next tool."
        elif "timeout" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Claude API request timed out. Retrying in fallback chain."
        elif "context_length_exceeded" in error_message.lower():
            recovery = "fallback_to_next_tool"
            user_message = "Context too long for Claude. Switching to next tool."
        else:
            recovery = "fallback_to_next_tool"
            user_message = f"Claude API error: {error_type}. Switching to next tool."

        return {
            "status": "error",
            "error": error_message,
            "error_type": error_type,
            "recovery": recovery,
            "user_message": user_message,
            "tool": "claude"
        }

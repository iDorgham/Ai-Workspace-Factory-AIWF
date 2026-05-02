"""
Gemini Tool Adapter

Integrates with Google Generative AI for text and vision tasks.
Specializes in multimodal (text + image) processing, fast latency.
"""

import time
import os
from .base_adapter import ToolAdapter

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class GeminiAdapter(ToolAdapter):
    """Gemini tool adapter for Google Generative AI integration"""

    # Pricing (April 2026)
    INPUT_PRICE_PER_1K = 0.0005      # $0.0005 per 1K input tokens
    OUTPUT_PRICE_PER_1K = 0.0015     # $0.0015 per 1K output tokens

    def __init__(self, api_key: str = None, config: dict = None):
        """Initialize Gemini adapter with multimodal support."""
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        config = config or {}
        super().__init__("gemini", api_key, config)

        if genai is None:
            raise ImportError("google-generativeai package required. Install: pip install google-generativeai")

        # Configure API key
        genai.configure(api_key=api_key)

        # Configuration
        self.model = config.get("model", "gemini-pro")
        self.vision_model = config.get("vision_model", "gemini-pro-vision")
        self.temperature = config.get("temperature", 1.0)

    def execute(self, command: str, images: list = None, **kwargs) -> dict:
        """Execute command via Gemini API with optional image support."""
        start_time = time.time()

        try:
            # Determine if using vision model
            has_images = images and len(images) > 0
            model_name = self.vision_model if has_images else self.model

            # Get model
            model = genai.GenerativeModel(model_name)

            # Prepare content
            if has_images:
                # Multimodal: text + images
                content_parts = [command]
                for image_path in images:
                    try:
                        img = genai.upload_file(image_path)
                        content_parts.append(img)
                    except Exception as e:
                        # Fallback if image can't be loaded
                        pass
                response = model.generate_content(content_parts)
            else:
                # Text only
                response = model.generate_content(command)

            # Extract data
            output_text = response.text
            input_tokens = response.usage_metadata.prompt_tokens if hasattr(response, 'usage_metadata') else len(command) // 4
            output_tokens = response.usage_metadata.completion_tokens if hasattr(response, 'usage_metadata') else len(output_text) // 4

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
                "model": model_name
            }

        except Exception as e:
            latency = time.time() - start_time
            self.update_stats(success=False, error=str(e))
            self.track_performance(latency, False)
            return self.handle_error(e)

    def count_tokens(self, text: str, images: list = None, **kwargs) -> int:
        """Count tokens including image tokens."""
        # Approximation: text ~4 chars per token, images ~256 tokens each
        text_tokens = len(text) // 4
        image_tokens = (len(images) * 256) if images else 0
        return text_tokens + image_tokens

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with Gemini pricing (cheapest)."""
        input_cost = (input_tokens / 1000) * self.INPUT_PRICE_PER_1K
        output_cost = (output_tokens / 1000) * self.OUTPUT_PRICE_PER_1K
        return round(input_cost + output_cost, 6)

    def handle_error(self, error: Exception) -> dict:
        """Handle Gemini-specific errors."""
        error_type = type(error).__name__
        error_message = str(error)

        # Classify error
        if "rate_limit" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Gemini API rate limit exceeded. Retrying..."
        elif "invalid" in error_message.lower():
            recovery = "fallback_to_next_tool"
            user_message = "Invalid request to Gemini. Switching to next tool."
        elif "authentication" in error_message.lower() or "401" in error_message:
            recovery = "fallback_to_next_tool"
            user_message = "Authentication failed. Switching to next tool."
        elif "timeout" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Gemini request timed out. Retrying..."
        else:
            recovery = "fallback_to_next_tool"
            user_message = f"Gemini error. Switching to next tool."

        return {
            "status": "error",
            "error": error_message,
            "error_type": error_type,
            "recovery": recovery,
            "user_message": user_message,
            "tool": "gemini"
        }

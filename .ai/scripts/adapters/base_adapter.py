"""
Base ToolAdapter Abstract Class

Defines the interface for all tool adapters (Claude, Gemini, Copilot, Codex, etc).
Each adapter provides real API integration with token counting, cost calculation,
error handling, and performance tracking.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import time
from datetime import datetime


class ToolAdapter(ABC):
    """
    Abstract base class for all tool adapters.

    Defines the interface that all tool adapters must implement:
    - Claude, Gemini, Copilot, Codex, Qwen, OpenCode, Kilo

    Each adapter provides:
    - Real API integration
    - Token counting
    - Cost calculation
    - Error handling
    - Performance tracking
    """

    def __init__(self, tool_name: str, api_key: str, config: Dict = None):
        """
        Initialize adapter with configuration.

        Args:
            tool_name (str): Name of the tool (claude, gemini, copilot, codex, etc)
            api_key (str): API key for authentication
            config (Dict): Configuration options specific to tool
        """
        self.tool_name = tool_name
        self.api_key = api_key
        self.config = config or {}

        # Initialize statistics tracking
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0.0,
            "total_latency": 0.0,
            "avg_latency_ms": 0.0,
            "min_latency_ms": float('inf'),
            "max_latency_ms": 0.0,
            "last_error": None,
            "last_error_time": None,
            "consecutive_failures": 0,
            "success_rate": 0.0,
            "first_request_at": None,
            "last_request_at": None
        }

    # ========== ABSTRACT METHODS (must implement) ==========

    @abstractmethod
    def execute(self, command: str, **kwargs) -> Dict:
        """
        Execute a command via the tool API.

        Args:
            command (str): The command/prompt to execute
            **kwargs: Additional tool-specific arguments

        Returns:
            Dict with status, output, tokens, cost, latency
        """
        pass

    @abstractmethod
    def count_tokens(self, text: str, **kwargs) -> int:
        """Count tokens in text for cost calculation."""
        pass

    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage and tool pricing."""
        pass

    @abstractmethod
    def handle_error(self, error: Exception) -> Dict:
        """Handle tool-specific errors and suggest recovery strategy."""
        pass

    # ========== CONCRETE METHODS (same for all adapters) ==========

    def track_performance(self, execution_time: float, success: bool) -> None:
        """Track performance metrics."""
        latency_ms = execution_time * 1000

        # Update statistics
        self.stats["total_latency"] += execution_time
        self.stats["min_latency_ms"] = min(self.stats["min_latency_ms"], latency_ms)
        self.stats["max_latency_ms"] = max(self.stats["max_latency_ms"], latency_ms)

        # Update average using exponential moving average (EMA)
        alpha = 0.3  # Weight for new measurement
        current_avg = self.stats["avg_latency_ms"]
        self.stats["avg_latency_ms"] = (
            current_avg * (1 - alpha) + latency_ms * alpha
        )

        # Update success metrics
        if success:
            self.stats["consecutive_failures"] = 0
        else:
            self.stats["consecutive_failures"] += 1

        # Update timestamp
        self.stats["last_request_at"] = datetime.now().isoformat()
        if self.stats["first_request_at"] is None:
            self.stats["first_request_at"] = self.stats["last_request_at"]

    def update_stats(self,
                     input_tokens: int = 0,
                     output_tokens: int = 0,
                     cost: float = 0.0,
                     success: bool = True,
                     error: str = None) -> None:
        """Update adapter statistics after each execution."""
        self.stats["total_requests"] += 1
        self.stats["total_input_tokens"] += input_tokens
        self.stats["total_output_tokens"] += output_tokens
        self.stats["total_cost"] += cost

        if success:
            self.stats["successful_requests"] += 1
        else:
            self.stats["failed_requests"] += 1
            self.stats["last_error"] = error
            self.stats["last_error_time"] = datetime.now().isoformat()

        # Calculate success rate
        total = self.stats["total_requests"]
        if total > 0:
            self.stats["success_rate"] = (
                self.stats["successful_requests"] / total * 100
            )

    def get_stats(self) -> Dict:
        """Get current adapter statistics."""
        return {
            "tool": self.tool_name,
            "total_requests": self.stats["total_requests"],
            "successful_requests": self.stats["successful_requests"],
            "failed_requests": self.stats["failed_requests"],
            "success_rate": round(self.stats["success_rate"], 2),
            "total_input_tokens": self.stats["total_input_tokens"],
            "total_output_tokens": self.stats["total_output_tokens"],
            "total_cost": round(self.stats["total_cost"], 6),
            "avg_latency_ms": round(self.stats["avg_latency_ms"], 2),
            "min_latency_ms": round(self.stats["min_latency_ms"], 2) if self.stats["min_latency_ms"] != float('inf') else 0,
            "max_latency_ms": round(self.stats["max_latency_ms"], 2),
            "total_latency_seconds": round(self.stats["total_latency"], 2),
            "consecutive_failures": self.stats["consecutive_failures"],
            "last_error": self.stats["last_error"],
            "last_error_time": self.stats["last_error_time"],
            "first_request_at": self.stats["first_request_at"],
            "last_request_at": self.stats["last_request_at"]
        }

    def reset_stats(self) -> None:
        """Reset all statistics (useful for testing)."""
        self.__init__(self.tool_name, self.api_key, self.config)

    def get_health_status(self) -> str:
        """Get adapter health status based on statistics."""
        if self.stats["total_requests"] == 0:
            return "UNKNOWN"

        success_rate = self.stats["success_rate"]
        avg_latency = self.stats["avg_latency_ms"]
        consecutive_failures = self.stats["consecutive_failures"]

        # OFFLINE: No successes or recent consecutive failures
        if success_rate == 0 or consecutive_failures > 5:
            return "OFFLINE"

        # DEGRADED: Low success rate or high latency
        if success_rate < 80 or avg_latency > 10000:
            return "DEGRADED"

        # HEALTHY: Good success rate and reasonable latency
        return "HEALTHY"

    def format_cost(self) -> str:
        """Return formatted cost string."""
        return f"${self.stats['total_cost']:.6f}"

    def format_latency(self) -> str:
        """Return formatted latency string."""
        return f"{self.stats['avg_latency_ms']:.0f}ms"

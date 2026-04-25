"""
Base ToolAdapter Abstract Class

Defines the interface for all tool adapters (Claude, Gemini, Copilot, Codex, etc).
Each adapter provides real API integration with token counting, cost calculation,
error handling, and performance tracking.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


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

    # ========== PERFORMANCE LEDGER (F5 Brainstorm Signal) ==========

    def _get_session_id(self) -> str:
        """Return git HEAD short SHA as session identifier."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=3
            )
            return result.stdout.strip() if result.returncode == 0 else "no-git"
        except Exception:
            return "no-git"

    def _make_reasoning_hash(self, tool_name: str, timestamp: str) -> str:
        """Deterministic hash: adapter + tool + timestamp."""
        raw = f"{self.tool_name}:{tool_name}:{timestamp}"
        return f"sha256:{hashlib.sha256(raw.encode()).hexdigest()[:16]}"

    def _find_ledger_path(self) -> Path:
        """Locate tool_performance.jsonl relative to repo root."""
        # Walk up from this file's location to find .ai/logs/ledgers/
        current = Path(__file__).resolve()
        for parent in current.parents:
            candidate = parent / ".ai" / "logs" / "ledgers" / "tool_performance.jsonl"
            if candidate.exists():
                return candidate
        # Fallback: create relative to repo root guess
        return Path(__file__).resolve().parents[7] / ".ai" / "logs" / "ledgers" / "tool_performance.jsonl"

    def log_to_performance_ledger(
        self,
        tool: str,
        status: str,
        latency_ms: int,
        tokens_in: Optional[int] = None,
        tokens_out: Optional[int] = None,
        error_code: Optional[str] = None
    ) -> None:
        """
        Append a structured entry to .ai/logs/ledgers/tool_performance.jsonl.

        Called by concrete adapters after every tool invocation. Provides signal
        data for the F5 brainstorm intelligence layer to detect patterns, gaps,
        and adapter health across the multi-LLM stack.

        Args:
            tool: Function/method name invoked
            status: 'success' | 'error' | 'timeout' | 'rate_limited'
            latency_ms: Wall-clock duration in milliseconds
            tokens_in: Input token count (None if unavailable)
            tokens_out: Output token count (None if unavailable)
            error_code: Error code string if status != 'success'
        """
        now = datetime.now(timezone.utc).isoformat()
        entry = {
            "type": "tool_call",
            "adapter": self.tool_name,
            "tool": tool,
            "status": status,
            "latency_ms": latency_ms,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "error_code": error_code,
            "session_id": self._get_session_id(),
            "timestamp": now,
            "reasoning_hash": self._make_reasoning_hash(tool, now)
        }
        try:
            ledger = self._find_ledger_path()
            ledger.parent.mkdir(parents=True, exist_ok=True)
            with open(ledger, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception:
            # Never let ledger writes crash tool execution
            pass

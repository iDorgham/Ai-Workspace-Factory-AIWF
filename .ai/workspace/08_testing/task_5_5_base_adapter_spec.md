# Task 5.5: Base ToolAdapter Class Specification

**Day:** 5  
**Task:** 5.5  
**Duration:** 2 hours  
**Status:** READY TO IMPLEMENT

---

## Overview

Create the abstract base class `ToolAdapter` that defines the interface for all tool adapters (Claude, Gemini, Copilot, Codex). This class provides the contract that all adapters must implement.

---

## File Location
```
.ai/scripts/adapters/[tool]-adapter.py
```

---

## Complete Implementation

```python
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
                - model: Model name to use
                - max_tokens: Maximum output tokens
                - temperature: Sampling temperature
                - timeout: Request timeout in seconds
                - system_prompt: Optional system instruction
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
        
        This is the main method that subclasses must implement.
        Each adapter will have tool-specific implementation details.
        
        Args:
            command (str): The command/prompt to execute
            **kwargs: Additional tool-specific arguments
            
        Returns:
            Dict with keys:
                - status: "success" or "error"
                - output: Generated output (on success)
                - input_tokens: Number of input tokens
                - output_tokens: Number of output tokens
                - cost: Cost in USD
                - latency: Execution time in seconds
                - model: Model used
                - error: Error message (on failure)
                - error_type: Type of error (on failure)
                - recovery: Recovery strategy (on failure)
        
        Example return (success):
            {
                "status": "success",
                "output": "Generated text...",
                "input_tokens": 1250,
                "output_tokens": 3400,
                "cost": 0.03435,
                "latency": 2.145,
                "model": "claude-opus-4-6"
            }
        
        Example return (error):
            {
                "status": "error",
                "error": "Rate limit exceeded",
                "error_type": "RateLimitError",
                "recovery": "retry_with_backoff",
                "tool": "claude"
            }
        """
        pass
    
    @abstractmethod
    def count_tokens(self, text: str, **kwargs) -> int:
        """
        Count tokens in text.
        
        Different tools may count tokens differently.
        This allows accurate cost and usage tracking.
        
        Args:
            text (str): Text to count
            **kwargs: Additional arguments (e.g., for images)
            
        Returns:
            int: Number of tokens
        """
        pass
    
    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost based on token usage.
        
        Each tool has different pricing.
        
        Args:
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
            
        Returns:
            float: Cost in USD
        """
        pass
    
    @abstractmethod
    def handle_error(self, error: Exception) -> Dict:
        """
        Handle tool-specific errors.
        
        Classify errors and suggest recovery strategies.
        
        Args:
            error (Exception): The error that occurred
            
        Returns:
            Dict with keys:
                - status: "error"
                - error: Error message
                - error_type: Type of error
                - recovery: Recovery strategy
                - user_message: User-friendly message
        """
        pass
    
    # ========== CONCRETE METHODS (same for all adapters) ==========
    
    def track_performance(self, execution_time: float, success: bool) -> None:
        """
        Track performance metrics.
        
        Automatically called by execute() implementations.
        
        Args:
            execution_time (float): Time in seconds
            success (bool): Whether request succeeded
        """
        latency_ms = execution_time * 1000
        
        # Update statistics
        self.stats["total_latency"] += execution_time
        self.stats["min_latency_ms"] = min(self.stats["min_latency_ms"], latency_ms)
        self.stats["max_latency_ms"] = max(self.stats["max_latency_ms"], latency_ms)
        
        # Update average using exponential moving average (EMA)
        # EMA gives more weight to recent measurements
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
        """
        Update adapter statistics.
        
        Called after each execute() to track usage.
        
        Args:
            input_tokens (int): Input tokens used
            output_tokens (int): Output tokens used
            cost (float): Cost in USD
            success (bool): Whether request succeeded
            error (str): Error message if failed
        """
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
        """
        Get current adapter statistics.
        
        Returns:
            Dict with all tracked metrics
        """
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
            "min_latency_ms": round(self.stats["min_latency_ms"], 2),
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
        """
        Get adapter health status based on statistics.
        
        Returns:
            str: "HEALTHY", "DEGRADED", or "OFFLINE"
        """
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
```

---

## Integration Points

### In execute() Implementation:

```python
def execute(self, command: str) -> Dict:
    start_time = time.time()
    
    try:
        # 1. Call API
        response = self.api_call(command)
        
        # 2. Parse response
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        output_text = response.content[0].text
        
        # 3. Calculate cost
        cost = self.calculate_cost(input_tokens, output_tokens)
        
        # 4. Track latency
        latency = time.time() - start_time
        self.track_performance(latency, True)
        
        # 5. Update stats
        self.update_stats(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            success=True
        )
        
        # 6. Return formatted result
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
        self.track_performance(latency, False)
        self.update_stats(success=False, error=str(e))
        return self.handle_error(e)
```

---

## Inheritance Pattern

```python
# Base class
class ToolAdapter(ABC):
    def __init__(self, ...): ...
    @abstractmethod
    def execute(self): pass
    @abstractmethod
    def count_tokens(self): pass
    @abstractmethod
    def calculate_cost(self): pass
    @abstractmethod
    def handle_error(self): pass
    def track_performance(self): ...
    def update_stats(self): ...
    def get_stats(self): ...

# Subclass implementation
class ClaudeAdapter(ToolAdapter):
    def __init__(self, api_key, config=None):
        super().__init__("claude", api_key, config)
        # Claude-specific initialization
    
    def execute(self, command):
        # Claude-specific implementation
        pass
    
    def count_tokens(self, text):
        # Claude-specific token counting
        pass
    
    def calculate_cost(self, input_tokens, output_tokens):
        # Claude pricing calculation
        pass
    
    def handle_error(self, error):
        # Claude error handling
        pass
```

---

## Testing Base Class

```python
# All adapters inherit these methods - they're tested once
def test_stats_tracking():
    adapter = ClaudeAdapter(api_key)
    
    # Stats start empty
    assert adapter.stats["total_requests"] == 0
    
    # After execution, stats update
    result = adapter.execute("test")
    assert adapter.stats["total_requests"] == 1
    
    # Get stats returns proper format
    stats = adapter.get_stats()
    assert "tool" in stats
    assert "success_rate" in stats

def test_health_status():
    adapter = ClaudeAdapter(api_key)
    
    # Unknown before any requests
    assert adapter.get_health_status() == "UNKNOWN"
    
    # HEALTHY after successful requests
    adapter.execute("test 1")
    adapter.execute("test 2")
    assert adapter.get_health_status() == "HEALTHY"
```

---

**File Size:** ~200 lines  
**Status:** READY FOR IMPLEMENTATION  
**Duration:** 2 hours

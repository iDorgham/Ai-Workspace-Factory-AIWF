# Task 5.1: Claude Adapter Implementation Specification

**Day:** 5  
**Task:** 5.1  
**Duration:** 4 hours  
**Status:** READY TO IMPLEMENT

---

## Overview

Implement a production-ready Claude tool adapter that integrates with the existing ToolRouter from Phase 1. This adapter will replace the mock Claude execution with real API calls to Claude via the Anthropic SDK.

---

## Objectives

1. ✅ Create `ClaudeAdapter` class inheriting from `ToolAdapter` base class
2. ✅ Implement real Claude API integration via Anthropic SDK
3. ✅ Token counting and cost calculation
4. ✅ Error handling with graceful recovery
5. ✅ Performance tracking (latency, success rate)
6. ✅ Comprehensive test coverage (5 test cases)
7. ✅ Integration with ToolRouter for real execution

---

## Architecture

### Class Hierarchy

```
ToolAdapter (Abstract Base Class)
    ↓
ClaudeAdapter (Production Implementation)
    ├─ execute(command) → Dict
    ├─ count_tokens(text) → int
    ├─ calculate_cost(input_tokens, output_tokens) → float
    ├─ handle_error(exception) → Dict
    └─ track_performance(execution_time, success) → None
```

### Integration Point

```
ToolRouter (Phase 1)
    ↓
Tool Selection Logic (existing)
    ↓
ClaudeAdapter.execute() ← NEW (Real API)
    ├─ Anthropic SDK
    ├─ Token counting
    ├─ Cost calculation
    └─ Error handling
    ↓
Logging (workflow.jsonl)
    ↓
Response to User
```

---

## Implementation Details

### File Location
```
.ai/scripts/adapters/[tool]-adapter.py
```

### Dependencies
```python
from anthropic import Anthropic
from anthropic.types.message import Message
from abc import ABC, abstractmethod
import time
import json
```

### Configuration

Claude adapter needs these environment variables:
```bash
CLAUDE_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-opus-4-6 (default)
CLAUDE_MAX_TOKENS=4096 (default)
```

### Base Class Interface (Reference)

```python
class ToolAdapter(ABC):
    """Abstract base class for all tool adapters"""
    
    def __init__(self, tool_name: str, api_key: str, config: Dict):
        self.tool_name = tool_name
        self.api_key = api_key
        self.config = config
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cost": 0.0,
            "avg_latency_ms": 0,
            "last_error": None
        }
    
    @abstractmethod
    def execute(self, command: str) -> Dict:
        """Execute a command via the tool"""
        pass
    
    @abstractmethod
    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        pass
    
    @abstractmethod
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token counts"""
        pass
    
    @abstractmethod
    def handle_error(self, error: Exception) -> Dict:
        """Handle tool-specific errors"""
        pass
    
    def track_performance(self, execution_time: float, success: bool) -> None:
        """Track performance metrics"""
        pass
```

---

## Implementation Specification

### ClaudeAdapter Class

```python
class ClaudeAdapter(ToolAdapter):
    """Claude tool adapter for Anthropic API integration"""
    
    # Pricing (from Anthropic pricing page, April 2026)
    INPUT_PRICE_PER_1K = 0.003      # $0.003 per 1K input tokens
    OUTPUT_PRICE_PER_1K = 0.009     # $0.009 per 1K output tokens
    
    def __init__(self, api_key: str, config: Dict = None):
        """
        Initialize Claude adapter
        
        Args:
            api_key (str): Anthropic API key
            config (Dict): Configuration options
                - model (str): Claude model (default: claude-opus-4-6)
                - max_tokens (int): Max output tokens (default: 4096)
                - temperature (float): Sampling temperature (default: 1.0)
                - system_prompt (str): System prompt (default: none)
        """
        config = config or {}
        super().__init__("claude", api_key, config)
        
        # Initialize Anthropic client
        self.client = Anthropic(api_key=api_key)
        
        # Configuration
        self.model = config.get("model", "claude-opus-4-6")
        self.max_tokens = config.get("max_tokens", 4096)
        self.temperature = config.get("temperature", 1.0)
        self.system_prompt = config.get("system_prompt", None)
        
    def execute(self, command: str) -> Dict:
        """
        Execute a command via Claude API
        
        Args:
            command (str): User command/prompt
            
        Returns:
            Dict with keys:
                - status: "success" or "error"
                - output: Generated text (on success)
                - input_tokens: Number of input tokens used
                - output_tokens: Number of output tokens generated
                - cost: Cost in USD
                - latency: Execution time in seconds
                - error: Error message (on failure)
                - error_type: Type of error (on failure)
        """
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
            self.stats["total_requests"] += 1
            self.stats["successful_requests"] += 1
            self.stats["total_input_tokens"] += input_tokens
            self.stats["total_output_tokens"] += output_tokens
            self.stats["total_cost"] += cost
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
            self.stats["total_requests"] += 1
            self.stats["failed_requests"] += 1
            self.stats["last_error"] = str(e)
            self.track_performance(latency, False)
            
            return self.handle_error(e)
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text using Claude's tokenizer
        
        Args:
            text (str): Text to count
            
        Returns:
            int: Number of tokens
        """
        try:
            # Use Anthropic's token counting
            # Note: Approximation method (Claude uses ~4 chars per token on average)
            # For production, use the official token counter when available
            return len(text) // 4
        except Exception:
            # Fallback to character-based estimation
            return len(text) // 4
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate cost based on token usage
        
        Args:
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
            
        Returns:
            float: Cost in USD
        """
        input_cost = (input_tokens / 1000) * self.INPUT_PRICE_PER_1K
        output_cost = (output_tokens / 1000) * self.OUTPUT_PRICE_PER_1K
        return round(input_cost + output_cost, 6)
    
    def handle_error(self, error: Exception) -> Dict:
        """
        Handle Claude-specific errors
        
        Args:
            error (Exception): The error that occurred
            
        Returns:
            Dict with error details
        """
        error_type = type(error).__name__
        error_message = str(error)
        
        # Classify error and suggest recovery
        if "rate_limit" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Claude API rate limit exceeded. Retrying in fallback chain."
        elif "invalid_request" in error_message.lower():
            recovery = "fallback_to_next_tool"
            user_message = "Invalid request to Claude API. Switching to next tool."
        elif "authentication" in error_message.lower():
            recovery = "fallback_to_next_tool"
            user_message = "Authentication failed with Claude API. Switching to next tool."
        elif "timeout" in error_message.lower():
            recovery = "retry_with_backoff"
            user_message = "Claude API request timed out. Retrying in fallback chain."
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
    
    def track_performance(self, execution_time: float, success: bool) -> None:
        """
        Track performance metrics
        
        Args:
            execution_time (float): Time in seconds
            success (bool): Whether request succeeded
        """
        # Update latency (exponential moving average)
        current_avg = self.stats.get("avg_latency_ms", 0)
        new_latency_ms = execution_time * 1000
        
        # EMA with alpha=0.3
        self.stats["avg_latency_ms"] = (
            current_avg * 0.7 + new_latency_ms * 0.3
        )
    
    def get_stats(self) -> Dict:
        """Get current adapter statistics"""
        total = self.stats["total_requests"]
        success_rate = (
            self.stats["successful_requests"] / total * 100
            if total > 0 else 0
        )
        
        return {
            "tool": "claude",
            "total_requests": total,
            "successful_requests": self.stats["successful_requests"],
            "failed_requests": self.stats["failed_requests"],
            "success_rate": round(success_rate, 2),
            "total_input_tokens": self.stats["total_input_tokens"],
            "total_output_tokens": self.stats["total_output_tokens"],
            "total_cost": round(self.stats["total_cost"], 6),
            "avg_latency_ms": round(self.stats["avg_latency_ms"], 2),
            "last_error": self.stats["last_error"]
        }
```

---

## Testing Specification

### Test File Location
```
tests/day-5-claude-adapter-tests.json
```

### Test Case 1: Simple Command Execution

**Name:** Simple text generation  
**Input:** "Write a short description of interior design"  
**Expected:**
- status: "success"
- output: non-empty string
- input_tokens: > 0
- output_tokens: > 0
- cost: > 0
- latency: > 0

**Validation:**
- Response contains expected fields
- Output length > 0
- Cost calculation correct (tokens * price)
- Latency reasonable (< 10 seconds)

### Test Case 2: Long Context Handling

**Name:** Large input text processing  
**Input:** Very long prompt (2000+ words)  
**Expected:**
- status: "success"
- Handles large context without error
- Token counts reflect actual size
- Cost reflects token usage

**Validation:**
- No truncation errors
- Token counting accurate
- Cost calculation correct

### Test Case 3: Rate Limit Handling

**Name:** Graceful rate limit error  
**Input:** Rapid successive commands  
**Expected:**
- status: "error"
- error_type: "RateLimitError" (or similar)
- recovery: "retry_with_backoff"
- Error message clear and actionable

**Validation:**
- Error properly classified
- Recovery strategy suggested
- Stats updated correctly

### Test Case 4: Error Recovery

**Name:** API error handling  
**Input:** Invalid/malformed request (if testable)  
**Expected:**
- status: "error"
- error_type: identified correctly
- recovery: "fallback_to_next_tool"
- user_message: helpful

**Validation:**
- Error type detected
- Recovery strategy sensible
- No unhandled exceptions

### Test Case 5: Performance Metrics

**Name:** Metrics tracking accuracy  
**Input:** Multiple successful requests  
**Expected:**
- stats.total_requests: incremented
- stats.successful_requests: incremented
- stats.total_cost: accumulated
- stats.avg_latency_ms: calculated

**Validation:**
- Stats accumulate correctly
- Cost totals are accurate
- Latency average calculated properly
- Success rate computed correctly

---

## Test Runner Implementation

### File Location
```
.ai/scripts/test-[tool]-adapter.py
```

### Test Runner Structure

```python
import json
import time
import os
from claude_adapter import ClaudeAdapter

class ClaudeAdapterTestRunner:
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.test_results = []
        self.passed = 0
        self.failed = 0
    
    def setup(self):
        """Initialize adapter for testing"""
        if not self.api_key:
            raise ValueError("CLAUDE_API_KEY environment variable not set")
        
        self.adapter = ClaudeAdapter(self.api_key)
    
    def run_test(self, test_case: Dict) -> bool:
        """Run a single test case"""
        test_id = test_case["test_id"]
        test_name = test_case["name"]
        
        try:
            # Execute test
            result = self.adapter.execute(test_case["input"])
            
            # Validate result
            validations = test_case.get("validations", [])
            all_pass = True
            
            for validation in validations:
                # Perform each validation
                passed = self._validate(result, validation)
                if not passed:
                    all_pass = False
            
            if all_pass:
                self.passed += 1
                self.test_results.append({
                    "test_id": test_id,
                    "name": test_name,
                    "status": "PASS",
                    "result": result
                })
                return True
            else:
                self.failed += 1
                self.test_results.append({
                    "test_id": test_id,
                    "name": test_name,
                    "status": "FAIL",
                    "result": result
                })
                return False
                
        except Exception as e:
            self.failed += 1
            self.test_results.append({
                "test_id": test_id,
                "name": test_name,
                "status": "ERROR",
                "error": str(e)
            })
            return False
    
    def run_all_tests(self):
        """Run all test cases"""
        with open("tests/day-5-claude-adapter-tests.json") as f:
            tests = json.load(f)
        
        for test_case in tests:
            self.run_test(test_case)
    
    def save_results(self):
        """Save results to JSON"""
        results = {
            "run_date": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "adapter": "claude",
            "tests_run": len(self.test_results),
            "tests_passed": self.passed,
            "tests_failed": self.failed,
            "pass_rate": f"{self.passed / len(self.test_results) * 100:.1f}%",
            "test_results": self.test_results,
            "adapter_stats": self.adapter.get_stats()
        }
        
        with open("logs/day-[day]-[report]-results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        return results

if __name__ == "__main__":
    runner = ClaudeAdapterTestRunner()
    runner.setup()
    runner.run_all_tests()
    results = runner.save_results()
    
    print(f"\n{'='*60}")
    print(f"Claude Adapter Tests: {results['tests_passed']}/{results['tests_run']} PASS")
    print(f"Pass Rate: {results['pass_rate']}")
    print(f"{'='*60}")
```

---

## Integration with ToolRouter

### Modification to ToolRouter

In `.ai/scripts/tool-router.py`, modify the `execute_tool()` method:

```python
def execute_tool(self, tool: str, command: str) -> Dict:
    """
    Execute a command using real tool adapters (not mocks)
    
    Args:
        tool (str): Tool name (claude, gemini, copilot, codex)
        command (str): Command to execute
        
    Returns:
        Dict with execution result
    """
    if tool == "claude":
        from adapters.claude_adapter import ClaudeAdapter
        adapter = ClaudeAdapter(
            api_key=os.getenv("CLAUDE_API_KEY"),
            config={"model": "claude-opus-4-6", "max_tokens": 4096}
        )
        return adapter.execute(command)
    
    # ... similar for other tools ...
    
    else:
        return {"status": "error", "error": f"Unknown tool: {tool}"}
```

---

## Logging Integration

### Workflow Entry Format

Each Claude adapter execution should log to `logs/workflow.jsonl`:

```json
{
  "timestamp": "2026-04-13T10:30:00Z",
  "event": "command_executed",
  "command": "/create blog-posts",
  "tool": "claude",
  "tool_rank": 1,
  "status": "success",
  "input_tokens": 1250,
  "output_tokens": 3400,
  "cost": 0.03435,
  "latency_ms": 2145,
  "model": "claude-opus-4-6",
  "error_type": null
}
```

---

## Success Criteria

✅ **Functionality**
- [ ] Claude adapter executes commands successfully
- [ ] Token counting works accurately
- [ ] Cost calculation matches Anthropic pricing
- [ ] Error handling graceful and informative
- [ ] Performance metrics tracked correctly

✅ **Testing**
- [ ] All 5 test cases pass
- [ ] Tests validate key functionality
- [ ] Results saved to JSON
- [ ] Test runner executable

✅ **Integration**
- [ ] Works with existing ToolRouter
- [ ] Logs to workflow.jsonl correctly
- [ ] API key management via environment
- [ ] No hardcoded secrets in code

✅ **Quality**
- [ ] Code well-documented
- [ ] Error messages clear
- [ ] Pricing accurate (April 2026 rates)
- [ ] Performance acceptable (< 10s per request)

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Setup & Base Class | 30 min | Ready |
| ClaudeAdapter Implementation | 2 hours | Ready |
| Test Spec & Runner | 1 hour | Ready |
| Integration & Validation | 30 min | Ready |
| **Total** | **4 hours** | **Ready** |

---

## Dependencies

```bash
# Required packages
pip install anthropic --break-system-packages

# Environment
export CLAUDE_API_KEY="sk-ant-..."
```

---

## What's Next

**After Task 5.1 Completes:**
1. Run 5 test cases: 5/5 PASS expected ✓
2. Save results to `logs/day-[day]-[report]-results.json`
3. Proceed to Task 5.2 (Gemini Adapter)
4. After all 4 adapters: Integrate with ToolRouter
5. Run Day 5 integration tests

**Then:**
- Day 6: Cost tracking system
- Day 7: Health monitoring & hardening

---

## Reference Materials

- Anthropic SDK: https://github.com/anthropic-ai/anthropic-sdk-python
- Claude Pricing: https://www.anthropic.com/pricing
- Token Counting: https://docs.anthropic.com/en/docs/resources/tokens
- API Reference: https://docs.anthropic.com/en/api/getting-started

---

**Specification Version:** 1.0  
**Created:** 2026-04-13  
**Status:** READY FOR IMPLEMENTATION  
**Estimated Duration:** 4 hours  
**Expected Test Pass Rate:** 100% (5/5)

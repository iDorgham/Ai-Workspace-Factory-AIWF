# Task 5.6: Day 5 Integration Guide

**Day:** 5  
**Task:** 5.6  
**Duration:** 2 hours  
**Status:** READY TO IMPLEMENT

---

## Overview

After implementing all 4 adapters (Claude, Gemini, Copilot, Codex), integrate them with the existing ToolRouter so real API calls replace mock execution.

---

## Integration Architecture

```
ToolRouter (Phase 1)
    ↓
Tool Selection Logic (existing)
    ↓
┌─ Real Adapters (new)
│  ├─ ClaudeAdapter()
│  ├─ GeminiAdapter()
│  ├─ CopilotAdapter()
│  └─ CodexAdapter()
│
└─ Fallback Chain on Error
   ├─ Try Rank 1 → Success: Return
   ├─ Rank 1 fails → Try Rank 2
   ├─ Rank 2 fails → Try Rank 3
   └─ All fail → Return error
```

---

## Modifications to ToolRouter

### 1. Import Adapters

```python
# At top of .ai/scripts/tool-router.py
import os
from adapters.base_adapter import ToolAdapter
from adapters.claude_adapter import ClaudeAdapter
from adapters.gemini_adapter import GeminiAdapter
from adapters.copilot_adapter import CopilotAdapter
from adapters.codex_adapter import CodexAdapter
```

### 2. Create Adapter Registry

```python
class ToolRouter:
    def __init__(self, ...):
        # ... existing code ...
        
        # Initialize adapters
        self.adapters = {
            "claude": ClaudeAdapter(
                api_key=os.getenv("CLAUDE_API_KEY"),
                config={"model": "claude-opus-4-6", "max_tokens": 4096}
            ),
            "gemini": GeminiAdapter(
                api_key=os.getenv("GEMINI_API_KEY"),
                config={"model": "gemini-pro"}
            ),
            "copilot": CopilotAdapter(
                api_key=os.getenv("COPILOT_API_KEY"),
                config={"model": "copilot"}
            ),
            "codex": CodexAdapter(
                api_key=os.getenv("CODEX_API_KEY"),
                config={"model": "code-davinci-003"}
            )
        }
```

### 3. Replace Mock Execution

**Before (mock execution):**
```python
def execute_tool(self, tool: str, command: str) -> Dict:
    if self.test_mode and tool in self.test_results:
        # Return test result (mock)
        test_result = self.test_results[tool]
        if test_result == "success":
            return {"status": "success", ...}
        else:
            return {"status": "error", ...}
```

**After (real adapters):**
```python
def execute_tool(self, tool: str, command: str) -> Dict:
    """Execute command via real tool adapter"""
    
    # Get adapter
    if tool not in self.adapters:
        return {
            "status": "error",
            "error": f"Tool not found: {tool}",
            "error_type": "tool_not_found"
        }
    
    adapter = self.adapters[tool]
    
    # Check API key
    if adapter.api_key is None:
        return {
            "status": "error",
            "error": f"API key not configured for {tool}",
            "error_type": "missing_api_key",
            "recovery": "fallback_to_next_tool"
        }
    
    # Execute via adapter
    try:
        result = adapter.execute(command)
        
        # Log to workflow.jsonl
        self.log_execution(tool, command, result)
        
        return result
        
    except Exception as e:
        # Log error
        self.log_error(tool, command, e)
        
        # Return error response
        return {
            "status": "error",
            "error": str(e),
            "error_type": type(e).__name__,
            "recovery": "fallback_to_next_tool",
            "tool": tool
        }
```

### 4. Update Normal Execution Mode

```python
def normal_execution_mode(self, command: str, preferred_tool: str = None) -> Dict:
    """
    Auto-select best tool with fallback chain
    
    NEW: Uses real adapters instead of mock
    """
    ranking = self.get_ranking_for_command(command)
    
    # Try each tool in ranking order
    for rank_position, tool_name in enumerate(ranking, 1):
        # Skip if API key not configured
        if tool_name not in self.adapters:
            continue
        
        # Execute via real adapter
        result = self.execute_tool(tool_name, command)
        
        # Log decision
        self.log_command(command, {
            "mode": "normal",
            "tool_selected": tool_name,
            "tool_rank": rank_position,
            "status": result.get("status")
        })
        
        # Success: return result
        if result.get("status") == "success":
            return result
        
        # Failure: log and continue to next tool in fallback
        error_type = result.get("error_type")
        if error_type not in ["recoverable_error", "rate_limit"]:
            # Non-recoverable error, skip fallback
            return result
    
    # All tools failed
    return {
        "status": "error",
        "error": "All tools in fallback chain failed",
        "error_type": "fallback_chain_exhausted"
    }
```

### 5. Update Logging

```python
def log_execution(self, tool: str, command: str, result: Dict) -> None:
    """Log command execution with real adapter details"""
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": "command_executed",
        "command": command[:100],  # First 100 chars
        "tool": tool,
        "status": result.get("status"),
        "input_tokens": result.get("input_tokens", 0),
        "output_tokens": result.get("output_tokens", 0),
        "cost": result.get("cost", 0),
        "latency_ms": round(result.get("latency", 0) * 1000, 2),
        "model": result.get("model"),
        "error_type": result.get("error_type") if result.get("status") == "error" else None
    }
    
    # Append to workflow.jsonl
    with open("logs/workflow.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

### 6. Add Adapter Statistics Endpoint

```python
def get_adapter_stats(self) -> Dict:
    """Get stats for all adapters"""
    return {
        tool: adapter.get_stats()
        for tool, adapter in self.adapters.items()
    }

def get_adapter_health(self) -> Dict:
    """Get health status of all adapters"""
    return {
        tool: adapter.get_health_status()
        for tool, adapter in self.adapters.items()
    }
```

---

## File Organization

```
.ai/scripts/
├── tool-router.py          ← Updated with adapter integration
├── adapters/
│   ├── __init__.py
│   ├── base-adapter.py     ← Base class (Task 5.5)
│   ├── claude-adapter.py   ← Claude (Task 5.1)
│   ├── gemini-adapter.py   ← Gemini (Task 5.2)
│   ├── copilot-adapter.py  ← Copilot (Task 5.3)
│   └── codex-adapter.py    ← Codex (Task 5.4)
├── test-claude-adapter.py
├── test-gemini-adapter.py
├── test-copilot-adapter.py
└── test-codex-adapter.py
```

---

## Environment Setup

Before running, set API keys:

```bash
# Claude
export CLAUDE_API_KEY="sk-ant-..."

# Gemini
export GEMINI_API_KEY="..."

# Copilot
export COPILOT_API_KEY="..."

# Codex
export CODEX_API_KEY="..."
```

Verify setup:

```bash
python3 -c "
import os
keys = ['CLAUDE_API_KEY', 'GEMINI_API_KEY', 'COPILOT_API_KEY', 'CODEX_API_KEY']
for key in keys:
    status = '✓' if os.getenv(key) else '✗'
    print(f'{status} {key}')
"
```

---

## Testing Integration

### Step 1: Test Each Adapter Individually

```bash
# Test Claude adapter
python3 .ai/scripts/test-[tool]-adapter.py

# Test Gemini adapter
python3 .ai/scripts/test-[tool]-adapter.py

# Test Copilot adapter
python3 .ai/scripts/test-[tool]-adapter.py

# Test Codex adapter
python3 .ai/scripts/test-[tool]-adapter.py
```

Expected: 5/5 tests PASS for each adapter

### Step 2: Test ToolRouter Integration

```bash
# Test normal mode with real adapters
python3 -c "
from scripts.tool_router import ToolRouter
router = ToolRouter(test_mode=False)  # Real mode
result = router.route_command('/create blog-posts')
print(f'Status: {result[\"status\"]}')
print(f'Tool used: {result.get(\"tool\")}')
"
```

Expected: Command executes with real Claude adapter

### Step 3: Test Fallback Chain

```bash
# Simulate Rank 1 failure -> Rank 2 fallback
# (may require mocking API errors)
```

### Step 4: Test All Modes

```bash
# Normal mode (auto-select)
result = router.route_command('/create blog-posts')

# Forced mode (specific tool)
result = router.route_command('/create blog-posts --tool gemini')

# Explain mode (show ranking)
result = router.route_command('/create blog-posts --explain-routing')

# Parallel mode (run 2 tools)
result = router.route_command('/create blog-posts --parallel')
```

---

## Logging Verification

After running commands, verify logs:

```bash
# Check workflow.jsonl
tail -5 logs/workflow.jsonl | python3 -m json.tool

# Expected output:
# {
#   "timestamp": "2026-04-13T10:30:00.123456",
#   "event": "command_executed",
#   "command": "/create blog-posts",
#   "tool": "claude",
#   "status": "success",
#   "input_tokens": 1250,
#   "output_tokens": 3400,
#   "cost": 0.03435,
#   "latency_ms": 2145.3,
#   "model": "claude-opus-4-6",
#   "error_type": null
# }
```

---

## Rollback Plan

If integration fails, fallback is available:

```bash
# Revert to mock execution (Days 1-4)
git checkout .ai/scripts/tool-router.py
# or manually change execute_tool() back to mock mode
```

---

## Success Criteria

✅ **Functionality**
- [ ] All 4 adapters initialized successfully
- [ ] Each adapter executes commands via real API
- [ ] Fallback chain works on failures
- [ ] All modes work (normal, explain, forced, parallel)

✅ **Logging**
- [ ] workflow.jsonl entries created
- [ ] Cost data captured accurately
- [ ] Token counts correct
- [ ] Latency measurements reasonable

✅ **Error Handling**
- [ ] Missing API keys handled gracefully
- [ ] API errors caught and logged
- [ ] Fallback activates on failure
- [ ] User gets helpful error messages

✅ **Integration**
- [ ] ToolRouter works with adapters
- [ ] Adapter statistics tracked
- [ ] Health status calculated
- [ ] No breaking changes to existing code

---

## Timeline

| Phase | Duration | Status |
|-------|----------|--------|
| Task 5.1: Claude | 4h | Ready |
| Task 5.2: Gemini | 4h | Ready |
| Task 5.3: Copilot | 4h | Ready |
| Task 5.4: Codex | 4h | Ready |
| Task 5.5: Base class | 2h | Ready |
| Task 5.6: Integration | 2h | Current |
| **Total Day 5** | **20h** | **On track** |

---

## Next Steps

After Day 5 Integration:
1. Run all 20 adapter tests → 20/20 PASS
2. Verify workflow.jsonl logging
3. Test all execution modes
4. Day 6: Cost tracking system
5. Day 7: Health monitoring

---

**Status:** READY FOR IMPLEMENTATION  
**Files to Modify:** 1 (tool-router.py)  
**Files to Create:** 0 (adapters already created)  
**Expected Test Pass Rate:** 100% (real adapters)

# Task 5.4: Codex Adapter Implementation Specification

**Day:** 5  
**Task:** 5.4  
**Duration:** 4 hours  
**Status:** READY TO IMPLEMENT

---

## Overview

Implement a production-ready Codex tool adapter specialized for bulk operations, fast execution, and cost-effective processing. This adapter integrates with OpenAI's Codex API and inherits from the `ToolAdapter` base class.

---

## Key Characteristics

| Aspect | Value |
|--------|-------|
| **API** | OpenAI Codex API |
| **Models** | code-davinci-003 |
| **Specialization** | Fast execution & bulk ops |
| **Pricing** | $0.002 / $0.006 |
| **Context** | 4K tokens |
| **Latency** | ~1.2s avg (FASTEST) |
| **Rank** | 2 (fallback or speed mode) |

---

## Ranking Strategy

**When Codex is Rank 1:**
```
/export csv             → Codex (fast bulk ops)
/bulk process content   → Codex (speed optimized)
/generate code snippets → Codex (rapid iteration)
```

**When Codex is Fallback (Rank 2-4):**
```
/create blog-posts      → Copilot → Codex → Gemini
/review code            → Copilot → Codex → Claude
```

---

## Implementation Details

### File Location
```
.ai/scripts/adapters/[tool]-adapter.py
```

### Dependencies
```bash
pip install openai --break-system-packages
```

### Environment Variables
```bash
CODEX_API_KEY=...
CODEX_MODEL=code-davinci-003 (default)
CODEX_MAX_TOKENS=2048 (default)
CODEX_TIMEOUT=5 (seconds, aggressive)
```

### Class Structure

```python
class CodexAdapter(ToolAdapter):
    """Codex adapter for fast execution and bulk operations"""
    
    # Pricing (April 2026)
    INPUT_PRICE_PER_1K = 0.002       # $0.002 per 1K tokens
    OUTPUT_PRICE_PER_1K = 0.006      # $0.006 per 1K tokens
    
    def __init__(self, api_key: str, config: Dict = None):
        """Initialize Codex adapter optimized for speed"""
        # OpenAI API client
        # Aggressive timeout for fast fallback
    
    def execute(self, command: str, mode: str = "standard") -> Dict:
        """
        Execute command optimized for speed and cost
        
        Args:
            command (str): Task description
            mode (str): "standard", "bulk", "fallback"
            
        Returns:
            Dict with execution result
        """
        # Fallback mode: reduce tokens, timeout faster
        # Bulk mode: batch processing optimization
        # Standard: normal execution
    
    def execute_bulk(self, commands: List[str]) -> List[Dict]:
        """Process multiple commands in batch"""
        # Optimized batch processing
        # Cost calculation for bulk
        pass
    
    def count_tokens(self, text: str) -> int:
        """Count tokens (usually fastest)"""
        pass
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with Codex pricing"""
        # Same as Copilot: $0.002 / $0.006
    
    def handle_error(self, error: Exception) -> Dict:
        """Handle Codex-specific errors with fast fallback"""
        # Timeout errors should be quick to detect
        pass
```

### Speed Optimization

```python
# Standard execution
response = adapter.execute("Generate Python code for...")

# Bulk operations (cost-effective)
commands = [
    "Translate line 1",
    "Translate line 2",
    "Translate line 3"
]
responses = adapter.execute_bulk(commands)

# Fallback mode (aggressive timeout)
response = adapter.execute(
    "Generate response",
    mode="fallback"  # 2s timeout instead of 10s
)
```

---

## Testing Strategy

**Test Cases (5 total):**

1. **Fast Execution** - Measure latency (< 2s target)
2. **Bulk Operations** - Process multiple commands
3. **Cost Efficiency** - Verify pricing same as Copilot
4. **Timeout Handling** - Fallback on timeout
5. **Batch Processing** - Large batch optimization

---

## Pricing Model

```
Input:  $0.002 per 1K tokens
Output: $0.006 per 1K tokens

Bulk discount example (10 commands):
├─ Individual: 10 × $0.0058 = $0.058
├─ Bulk: (9970 tokens / 1000 × 0.002) + (5800 / 1000 × 0.006)
└─ Savings: ~15% with batch optimization
```

---

## Speed Profile

**Latency Comparison:**
```
Codex:     1.2s avg  ✓ FASTEST
Copilot:   1.8s avg
Claude:    2.1s avg
Gemini:    0.85s avg (but only for vision)
Qwen:      2.5s avg
```

---

## Use in Fallback Chain

**When to use Codex in fallback:**

1. **Rank 2 fallback:** If Claude times out, try Codex
2. **Speed mode:** When latency matters more than quality
3. **Bulk operations:** Processing multiple items
4. **Cost-sensitive:** When budget is tight

---

**Status:** READY FOR IMPLEMENTATION

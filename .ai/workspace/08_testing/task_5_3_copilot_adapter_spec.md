# Task 5.3: Copilot Adapter Implementation Specification

**Day:** 5  
**Task:** 5.3  
**Duration:** 4 hours  
**Status:** READY TO IMPLEMENT

---

## Overview

Implement a production-ready Copilot tool adapter specialized for code generation and software development tasks. This adapter integrates with Microsoft's Copilot API and inherits from the `ToolAdapter` base class.

---

## Key Characteristics

| Aspect | Value |
|--------|-------|
| **API** | Microsoft Copilot API |
| **Models** | copilot (latest) |
| **Specialization** | Code generation & review |
| **Pricing** | $0.002 / $0.006 |
| **Context** | 8K tokens |
| **Latency** | ~1.8s avg |
| **Rank** | 1 (best for code tasks) |

---

## Use Cases

**Best For:**
- Code generation from description
- Code review and analysis
- Bug fixing and refactoring
- Documentation generation
- Architecture suggestions

**Ranking:**
```
/create blog-posts     → Copilot (Rank 1)
/optimize images       → Gemini (Rank 1)
/export                → Qwen (Rank 1)
/review code           → Copilot (Rank 1)
/generate docs         → Copilot (Rank 2)
```

---

## Implementation Details

### File Location
```
.ai/scripts/adapters/[tool]-adapter.py
```

### Dependencies
```bash
pip install openai --break-system-packages  # Uses OpenAI-compatible API
```

### Environment Variables
```bash
COPILOT_API_KEY=...
COPILOT_MODEL=copilot (default)
COPILOT_MAX_TOKENS=2048 (default)
```

### Class Structure

```python
class CopilotAdapter(ToolAdapter):
    """Copilot tool adapter for code generation and review"""
    
    # Pricing (April 2026)
    INPUT_PRICE_PER_1K = 0.002       # $0.002 per 1K tokens
    OUTPUT_PRICE_PER_1K = 0.006      # $0.006 per 1K tokens
    
    def __init__(self, api_key: str, config: Dict = None):
        """Initialize Copilot adapter for code tasks"""
        # OpenAI-compatible API client
        # Configuration for code-specific settings
    
    def execute(self, command: str, language: str = None) -> Dict:
        """
        Execute code generation/review task
        
        Args:
            command (str): Code task description or code to review
            language (str): Programming language (optional)
            
        Returns:
            Dict with execution result
        """
        # Detect code task type
        # Add language context if provided
        # Execute via Copilot API
    
    def analyze_code(self, code: str, analysis_type: str = "review") -> Dict:
        """
        Analyze code for issues, security, performance
        
        Args:
            code (str): Code to analyze
            analysis_type (str): "review", "security", "performance"
            
        Returns:
            Analysis results
        """
        pass
    
    def generate_code(self, description: str, language: str) -> Dict:
        """Generate code from description"""
        pass
    
    def count_tokens(self, text: str) -> int:
        """Count tokens for code (usually shorter)"""
        pass
    
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost with Copilot pricing"""
        # $0.002 / $0.006 (between Qwen and Claude)
    
    def handle_error(self, error: Exception) -> Dict:
        """Handle Copilot-specific errors"""
        pass
```

### Code-Specific Features

```python
# Generate code
response = adapter.execute(
    "Write a Python function to calculate factorial",
    language="python"
)

# Review existing code
response = adapter.analyze_code(
    code="def foo(x): return x*2",
    analysis_type="review"
)

# Security analysis
response = adapter.analyze_code(
    code="password = input('Enter password: ')",
    analysis_type="security"
)
```

---

## Testing Strategy

**Test Cases (5 total):**

1. **Code Generation** - Generate simple function
2. **Code Review** - Analyze provided code
3. **Language Support** - Multiple languages (Python, JS, etc)
4. **Error Detection** - Identify bugs in code
5. **Performance Metrics** - Latency tracking

---

## Pricing Model

```
Input:  $0.002 per 1K tokens
Output: $0.006 per 1K tokens

Example (500 input + 800 output tokens):
├─ Input: 500 / 1000 × $0.002 = $0.001
├─ Output: 800 / 1000 × $0.006 = $0.0048
└─ Total: $0.0058
```

---

## Context Size

**8K context limit** - Good for:
- Single file analysis
- Moderate-size code review
- Documentation from code

**Not ideal for:**
- Large codebase analysis (use fallback)
- Very long files (> 4K tokens)

---

**Status:** READY FOR IMPLEMENTATION

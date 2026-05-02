# CLI Layer — Flag Parser Implementation
**Phase 2a: Parsing & Validation**

---

## Overview

The flag parser extracts, validates, and processes CLI flags from user commands.

```
Input:  /create blog-posts --tool gemini --explain-routing
Output: {
  "command": "/create blog-posts",
  "flags": {
    "tool": "gemini",
    "tool_forced": true,
    "explain_routing": true,
    "prefer": null,
    "parallel": false
  },
  "valid": true
}
```

---

## Parsing Pipeline

### Step 1: Tokenize Input

```python
def tokenize(user_input):
    """
    Split input into tokens, preserving quoted strings.
    
    Example:
      Input: /create blog-posts --tool gemini
      Output: ["/create", "blog-posts", "--tool", "gemini"]
    """
    tokens = []
    current_token = ""
    in_quotes = False
    
    for char in user_input:
        if char == '"':
            in_quotes = not in_quotes
        elif char == " " and not in_quotes:
            if current_token:
                tokens.append(current_token)
                current_token = ""
        else:
            current_token += char
    
    if current_token:
        tokens.append(current_token)
    
    return tokens
```

### Step 2: Extract Command and Flags

```python
def extract_command_and_flags(tokens):
    """
    Separate command tokens from flag tokens.
    
    Commands start with / and end before first --flag
    Flags start with -- and include value or are boolean
    """
    command_tokens = []
    flag_tokens = []
    
    parsing_command = True
    i = 0
    
    while i < len(tokens):
        token = tokens[i]
        
        if token.startswith("--"):
            parsing_command = False
            flag_tokens.append(token)
        elif parsing_command and token.startswith("/"):
            command_tokens.append(token)
        elif parsing_command:
            command_tokens.append(token)
        else:
            flag_tokens.append(token)
        
        i += 1
    
    command = " ".join(command_tokens)
    return command, flag_tokens
```

### Step 3: Parse Flags into Dictionary

```python
def parse_flags(flag_tokens):
    """
    Convert flag tokens into dictionary.
    
    Examples:
      --tool gemini          → {"tool": "gemini"}
      --explain-routing      → {"explain_routing": true}
      --prefer qwen          → {"prefer": "qwen"}
      --parallel             → {"parallel": true}
    """
    flags = {
        "tool": None,
        "tool_forced": False,
        "explain_routing": False,
        "prefer": None,
        "parallel": False
    }
    
    i = 0
    while i < len(flag_tokens):
        token = flag_tokens[i]
        
        if token == "--tool" and i + 1 < len(flag_tokens):
            # --tool requires argument
            flags["tool"] = flag_tokens[i + 1]
            flags["tool_forced"] = True
            i += 2
        
        elif token == "--explain-routing":
            # Boolean flag
            flags["explain_routing"] = True
            i += 1
        
        elif token == "--prefer" and i + 1 < len(flag_tokens):
            # --prefer requires argument
            flags["prefer"] = flag_tokens[i + 1]
            i += 2
        
        elif token == "--parallel":
            # Boolean flag
            flags["parallel"] = True
            i += 1
        
        else:
            # Unknown flag
            i += 1
    
    return flags
```

### Step 4: Validate Flags

```python
def validate_flags(flags, tool_registry):
    """
    Check flags for:
    1. Valid tool names
    2. Tool availability
    3. Conflicting flag combinations
    4. Missing arguments
    """
    errors = []
    warnings = []
    
    # Validate --tool
    if flags["tool_forced"]:
        tool = flags["tool"]
        
        if tool not in tool_registry["tool_specs"]:
            errors.append(f"Tool '{tool}' not found in registry")
        else:
            if tool_registry["tool_specs"][tool]["status"] != "available":
                reason = tool_registry["tool_specs"][tool].get("reason", "unknown")
                errors.append(
                    f"Tool '{tool}' not available: {reason}. "
                    f"Available tools: {', '.join(tool_registry['available_tools'])}"
                )
    
    # Validate --prefer
    if flags["prefer"]:
        tool = flags["prefer"]
        
        if tool not in tool_registry["tool_specs"]:
            errors.append(f"Tool '{tool}' (--prefer) not found in registry")
        else:
            if tool_registry["tool_specs"][tool]["status"] != "available":
                reason = tool_registry["tool_specs"][tool].get("reason", "unknown")
                errors.append(
                    f"Tool '{tool}' (--prefer) not available: {reason}"
                )
    
    # Check for conflicting flags
    if flags["tool_forced"] and flags["explain_routing"]:
        errors.append(
            "--tool and --explain-routing are mutually exclusive. "
            "Choose: --tool to force execution, or --explain-routing to show why tool was selected"
        )
    
    if flags["parallel"] and flags["tool_forced"]:
        errors.append(
            "--parallel and --tool conflict. "
            "Use --parallel to run multiple tools, or --tool to force a single tool"
        )
    
    # Check if at least 2 tools available for --parallel
    if flags["parallel"]:
        available_count = len(
            [t for t in tool_registry["available_tools"]]
        )
        if available_count < 2:
            errors.append(
                "--parallel requires at least 2 tools available. "
                f"Currently available: {available_count}"
            )
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

---

## Flag Reference

### --tool [name]

**Purpose:** Force execution with specific tool, skip automatic selection

**Behavior:**
- Validates tool exists and is available
- Skips fallback chain (no retries if forced tool fails)
- Tool must be in available_tools list

**Examples:**
```bash
/create blog-posts --tool codex
/create blog-posts --tool gemini
/optimize images --tool qwen
```

**Conflicts:**
- Cannot combine with `--explain-routing`
- Cannot combine with `--parallel` (pick one tool or multiple)

**Response if unavailable:**
```
❌ Tool not available: opencode
Reason: not_installed

To enable:
  1. Install: pip install opencode-cli
  2. Run: /tool-setup opencode
  3. Verify: /list-available-tools

Available tools: copilot, codex, gemini, qwen
```

---

### --explain-routing

**Purpose:** Show why a tool would be selected (without executing)

**Behavior:**
- Looks up command in commands.md (MULTI-TOOL RANKINGS section)
- Shows tool ranking with performance metrics
- Returns explanation only, no content created
- Takes ~0.3s (no command execution)

**Examples:**
```bash
/create blog-posts --explain-routing
/optimize images --explain-routing
```

**Conflicts:**
- Cannot combine with `--tool` (conflicting intents)

**Output format:**
```
🧭 Tool Selection for /create blog-posts

Ranking & Performance:
  Rank 1: Copilot
    Latency: 3.5s | Cost: $0.003 | Success: 97%
    Why: Fast + moderate cost for content creation
  
  Rank 2: Codex
    Latency: 2.5s | Cost: $0.002 | Success: 96%
    Why: Cheaper, still fast, good fallback

Selected: Copilot (Rank 1)

To override:
  /create blog-posts --tool codex (force Codex)
  /create blog-posts --prefer qwen (prefer Qwen if Copilot fails)
```

---

### --prefer [name]

**Purpose:** Hint preference for fallback tool (does NOT force selection)

**Behavior:**
- Follows normal ranking (Rank 1 tool selected)
- If Rank 1 fails, skip to preferred tool (skip intermediate ranks)
- If preferred tool unavailable, error
- If Rank 1 succeeds, preference ignored

**Examples:**
```bash
/create blog-posts --prefer qwen
# Try Copilot first, but if it fails, use Qwen (not Codex)

/optimize images --prefer gemini
# Try Codex first, fallback to Gemini if Codex fails
```

**Behavior flowchart:**
```
Try Rank 1 (normal selection)
  ├─ Success? → Use Rank 1 output, ignore preference
  └─ Fail? → Check if preferred tool set
      ├─ Yes → Try preferred tool directly
      └─ No → Try Rank 2 (normal fallback)
```

---

### --parallel

**Purpose:** Run top 2 tools simultaneously, compare outputs

**Behavior:**
- Loads Rank 1 + Rank 2 tools
- Executes both concurrently (parallel threads)
- Creates both outputs (file_tool1_v1.md + file_tool2_v1.md)
- Returns side-by-side comparison
- Takes ~4.5s (not 8s sequential)

**Examples:**
```bash
/create blog-posts --parallel
# Creates: post_1_copilot_v1.md + post_1_codex_v1.md

/optimize images --parallel
# Creates: assets-seo_gemini_v1.json + assets-seo_codex_v1.json
```

**Conflicts:**
- Cannot combine with `--tool` (conflicting intents)

**Execution timeline:**
```
T=0s: Start Copilot (Rank 1) + Codex (Rank 2) simultaneously
T=2.5s: Codex returns
T=3.5s: Copilot returns
T=3.5s: Return both outputs + comparison summary

Total: 3.5s (instead of 6s sequential)
```

---

## Complete Parser Implementation

```python
def parse_cli_input(user_input, tool_registry):
    """
    Complete parsing pipeline.
    
    Returns:
      {
        "command": "/create blog-posts",
        "flags": {...},
        "valid": true/false,
        "errors": [...],
        "warnings": [...]
      }
    """
    # Step 1: Tokenize
    tokens = tokenize(user_input)
    
    # Step 2: Extract command and flags
    command, flag_tokens = extract_command_and_flags(tokens)
    
    # Step 3: Parse flags
    flags = parse_flags(flag_tokens)
    
    # Step 4: Validate flags
    validation = validate_flags(flags, tool_registry)
    
    return {
        "command": command,
        "flags": flags,
        "valid": validation["valid"],
        "errors": validation["errors"],
        "warnings": validation["warnings"]
    }


# Example usage
if __name__ == "__main__":
    import json
    
    # Load tool registry
    with open(".ai/tool-registry.json") as f:
        tool_registry = json.load(f)
    
    # Parse user input
    user_input = "/create blog-posts --tool gemini --explain-routing"
    result = parse_cli_input(user_input, tool_registry)
    
    print(json.dumps(result, indent=2))
```

---

## Integration with Guide-Agent

The parser is called in guide-agent's command execution flow:

```python
def execute_command(user_input):
    """Guide-agent command execution (updated)"""
    
    # Step 1: Load tool registry
    tool_registry = load_json(".ai/tool-registry.json")
    
    # Step 2: Parse CLI input (NEW)
    parse_result = parse_cli_input(user_input, tool_registry)
    
    # Step 3: Handle parsing errors
    if not parse_result["valid"]:
        return {
            "status": "error",
            "errors": parse_result["errors"],
            "suggestions": suggest_fixes(parse_result)
        }
    
    # Step 4: Extract parsed components
    command = parse_result["command"]
    flags = parse_result["flags"]
    
    # Step 5: Route to appropriate handler (in tool_router.md)
    return route_command(command, flags, tool_registry)
```

---

## Testing Examples

### Test 1: Valid Flag
```
Input: /create blog-posts --tool codex
Expected: {
  "valid": true,
  "command": "/create blog-posts",
  "flags": {"tool": "codex", "tool_forced": true, ...}
}
```

### Test 2: Invalid Tool
```
Input: /create blog-posts --tool qwen-chat
Expected: {
  "valid": false,
  "errors": ["Tool 'qwen-chat' not found in registry"]
}
```

### Test 3: Unavailable Tool
```
Input: /create blog-posts --tool opencode
Expected: {
  "valid": false,
  "errors": [
    "Tool 'opencode' not available: not_installed. ...",
    "Available tools: copilot, codex, gemini, qwen"
  ]
}
```

### Test 4: Conflicting Flags
```
Input: /create blog-posts --tool gemini --explain-routing
Expected: {
  "valid": false,
  "errors": [
    "--tool and --explain-routing are mutually exclusive"
  ]
}
```

### Test 5: Explain Routing (Valid)
```
Input: /create blog-posts --explain-routing
Expected: {
  "valid": true,
  "command": "/create blog-posts",
  "flags": {"explain_routing": true, "tool_forced": false, ...}
}
```

---

## Migration from Phase 1

Phase 1 commands (without flags) still work:

```bash
# Phase 1 (still works)
/create blog-posts

# Phase 2 (with flags)
/create blog-posts --tool copilot
/create blog-posts --explain-routing
/create blog-posts --prefer qwen
/create blog-posts --parallel
```

Parser returns same structure for both, flags are just empty/defaults.

---

## Next: Tool Router

Once flags are parsed and validated, they're passed to tool_router.md for execution decisions.

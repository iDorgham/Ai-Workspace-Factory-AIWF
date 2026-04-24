# CLI Layer Error Handling — Phase 2a

**Status:** Complete error response templates for all 4 flag parsing error cases.

---

## Error Categories & Response Templates

### 1. Invalid Tool Error

**Condition:** User specifies `--tool [name]` where `[name]` is not in `tool_registry.tool_specs`

**Response Template:**
```
❌ Tool Error: Invalid Tool Name

You specified: --tool [INVALID_TOOL_NAME]
Problem: '[INVALID_TOOL_NAME]' is not registered in this workspace.

✅ Available tools:
  • copilot    (Rank 1 - Quality)
  • codex      (Rank 2 - Speed/Cost)
  • gemini     (Rank 3 - Context/Multimodal)
  • qwen       (Rank 4 - Bulk/Cost)
  • opencode   (Rank 5 - Free/Dev)
  • kilo       (Rank 6 - TBD)

💡 Suggested Command:
  [ORIGINAL_COMMAND] --tool [CLOSEST_MATCH]

Example:
  /create blog-posts --tool qwen
```

**Implementation in guide-agent:**
```python
def error_invalid_tool(user_input, invalid_tool, available_tools, tool_registry):
    closest = find_closest_match(invalid_tool, available_tools)
    response = f"""❌ Tool Error: Invalid Tool Name

You specified: --tool {invalid_tool}
Problem: '{invalid_tool}' is not registered in this workspace.

✅ Available tools:
"""
    for tool in available_tools:
        rank = tool_registry["tool_specs"][tool].get("rank", "?")
        desc = tool_registry["tool_specs"][tool].get("optimization", "")
        response += f"  • {tool:12} (Rank {rank} - {desc})\n"
    
    response += f"""
💡 Suggested Command:
  {user_input.replace(f"--tool {invalid_tool}", f"--tool {closest}")}
"""
    return {"status": "error", "type": "invalid_tool", "message": response}
```

---

### 2. Unavailable Tool Error

**Condition:** User specifies `--tool [name]` where `[name]` is in registry but `status != "available"`

**Response Template:**
```
⚠️  Tool Error: Tool Not Available

You specified: --tool [TOOL_NAME]
Status: [STATUS] ([REASON])

Why unavailable:
  [DETAILED_REASON]

✅ Tools currently available:
  • [AVAILABLE_TOOL_1]
  • [AVAILABLE_TOOL_2]
  ...

💡 Options:
  A) Use an available tool:
     [ORIGINAL_COMMAND] --tool [RECOMMENDED_TOOL]

  B) Set up the unavailable tool:
     /tool-setup [TOOL_NAME]

  C) Use auto-selection (rank 1 + fallback chain):
     [ORIGINAL_COMMAND]
```

**Implementation in guide-agent:**
```python
def error_unavailable_tool(user_input, tool_name, tool_specs, available_tools):
    tool_info = tool_specs[tool_name]
    status = tool_info.get("status", "unknown")
    reason = tool_info.get("reason", "not configured")
    detailed = tool_info.get("detailed_reason", "No additional information available")
    
    response = f"""⚠️  Tool Error: Tool Not Available

You specified: --tool {tool_name}
Status: {status} ({reason})

Why unavailable:
  {detailed}

✅ Tools currently available:
"""
    for tool in available_tools:
        response += f"  • {tool}\n"
    
    # Find best alternative (highest rank among available)
    recommended = available_tools[0]  # Rank 1 available
    
    response += f"""
💡 Options:
  A) Use an available tool:
     {user_input.replace(f'--tool {tool_name}', f'--tool {recommended}')}

  B) Set up the unavailable tool:
     /tool-setup {tool_name}

  C) Use auto-selection (rank 1 + fallback chain):
     {user_input.replace(f' --tool {tool_name}', '')}
"""
    return {"status": "error", "type": "unavailable_tool", "message": response}
```

---

### 3. Conflicting Flags Error

**Condition:** User specifies mutually exclusive flag combinations:
- `--tool` + `--explain-routing` (can't force execution and explain at same time)
- `--tool` + `--parallel` (can't force single tool and run parallel)

**Response Template:**
```
❌ Flag Error: Conflicting Flags

You specified: [FLAG_1] [FLAG_2]
Problem: These flags cannot be used together.

[FLAG_1] means: [MEANING_1]
[FLAG_2] means: [MEANING_2]

Why they conflict:
  [CONFLICT_EXPLANATION]

💡 Choose one approach:

Option A: [DESCRIBE_OPTION_A]
  [ORIGINAL_COMMAND] [FLAG_OPTION_A]

Option B: [DESCRIBE_OPTION_B]
  [ORIGINAL_COMMAND] [FLAG_OPTION_B]

Option C: Run without flags (auto-select Rank 1 + fallback)
  [COMMAND_ONLY]
```

**Implementation (--tool + --explain-routing):**
```python
def error_tool_explain_conflict(user_input, command):
    response = """❌ Flag Error: Conflicting Flags

You specified: --tool [TOOL] --explain-routing
Problem: These flags cannot be used together.

--tool means:       "Force execution with this specific tool"
--explain-routing means: "Show me why the tool is selected (don't execute)"

Why they conflict:
  If you force a specific tool, there's no ranking to explain.
  If you want to see the ranking, you can't pre-force a tool.

💡 Choose one approach:

Option A: Force execution with specific tool (skip ranking explanation)
  """ + user_input.split(" --explain-routing")[0] + """

Option B: See ranking explanation before execution (auto-selects Rank 1)
  """ + user_input.split(" --tool")[0] + """ --explain-routing

Option C: Run without flags (auto-select Rank 1 + fallback)
  """ + command + """
"""
    return {"status": "error", "type": "conflicting_flags", "message": response}
```

**Implementation (--tool + --parallel):**
```python
def error_tool_parallel_conflict(user_input, command):
    response = """❌ Flag Error: Conflicting Flags

You specified: --tool [TOOL] --parallel
Problem: These flags cannot be used together.

--tool means:       "Force execution with exactly one specific tool"
--parallel means:   "Run top 2 tools simultaneously"

Why they conflict:
  --tool selects one tool. --parallel requires running 2+ tools.
  These are fundamentally opposite execution modes.

💡 Choose one approach:

Option A: Force single tool execution
  """ + user_input.split(" --parallel")[0] + """

Option B: Run top 2 tools in parallel (auto-selects Rank 1 & Rank 2)
  """ + user_input.split(" --tool")[0] + """ --parallel

Option C: Run without flags (auto-select Rank 1 + fallback)
  """ + command + """
"""
    return {"status": "error", "type": "conflicting_flags", "message": response}
```

---

### 4. Insufficient Tools for Parallel Error

**Condition:** User specifies `--parallel` but fewer than 2 tools are available

**Response Template:**
```
⚠️  Flag Error: Not Enough Tools for Parallel Execution

You specified: --parallel
Problem: --parallel requires 2+ available tools.

Available tools: [COUNT] ([TOOL_NAMES])
Required for --parallel: 2+ tools

💡 Options:
  A) Set up additional tools:
     /tool-setup [UNAVAILABLE_TOOL_1]
     /tool-setup [UNAVAILABLE_TOOL_2]

  B) Use auto-selection with fallback chain:
     [ORIGINAL_COMMAND]
     (Rank 1 executes; if it fails, Rank 2 auto-executes)

After setup, retry:
  [ORIGINAL_COMMAND] --parallel
```

**Implementation in guide-agent:**
```python
def error_insufficient_tools_parallel(user_input, command, available_count, available_tools, all_tools):
    unavailable = [t for t in all_tools if t not in available_tools]
    
    response = f"""⚠️  Flag Error: Not Enough Tools for Parallel Execution

You specified: --parallel
Problem: --parallel requires 2+ available tools.

Available tools: {available_count} ({', '.join(available_tools)})
Required for --parallel: 2+ tools

💡 Options:
  A) Set up additional tools:
"""
    for tool in unavailable[:2]:  # Suggest top 2
        response += f"     /tool-setup {tool}\n"
    
    response += f"""
  B) Use auto-selection with fallback chain:
     {command}
     (Rank 1 executes; if it fails, Rank 2 auto-executes)

After setup, retry:
  {user_input}
"""
    return {"status": "error", "type": "insufficient_tools", "message": response}
```

---

## Error Response Flow (in guide-agent)

```python
def handle_flag_validation_error(parse_result, user_input, command, tool_registry):
    """Route to appropriate error handler based on error type."""
    
    errors = parse_result["errors"]
    if not errors:
        return None  # No errors
    
    # Parse first error to determine type
    first_error = errors[0]
    
    if "not found in registry" in first_error:
        return error_invalid_tool(user_input, ...)
    
    elif "not available" in first_error:
        return error_unavailable_tool(user_input, ...)
    
    elif "mutually exclusive" in first_error:
        return error_tool_explain_conflict(user_input, command)
    
    elif "conflict" in first_error:
        return error_tool_parallel_conflict(user_input, command)
    
    elif "requires 2+ tools" in first_error:
        return error_insufficient_tools_parallel(user_input, command, ...)
    
    else:
        # Generic error fallback
        return {
            "status": "error",
            "type": "unknown",
            "message": f"Flag parsing error: {first_error}\n\nTry: {command}"
        }
```

---

## Integration Point (in execute_user_command)

```python
def execute_user_command(user_input):
    # ... flag parsing from GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM-PHASE2A.md ...
    
    parse_result = parse_and_validate_flags(flag_tokens, tool_registry)
    
    if not parse_result["valid"]:
        # ERROR HANDLING (THIS FILE)
        error_response = handle_flag_validation_error(
            parse_result, 
            user_input, 
            command,
            tool_registry
        )
        return error_response  # User sees friendly error + options
    
    # ... continue to Phase 1 routing ...
```

---

## Testing Error Handlers

### Test 1: Invalid Tool
```
Input: /create blog-posts --tool invalid
Expected: error_invalid_tool()
Output: List available tools + suggestion
```

### Test 2: Unavailable Tool
```
Input: /create blog-posts --tool opencode (if not installed)
Expected: error_unavailable_tool()
Output: Reason + /tool-setup suggestion + available alternatives
```

### Test 3: Conflicting Flags (--tool + --explain-routing)
```
Input: /create blog-posts --tool qwen --explain-routing
Expected: error_tool_explain_conflict()
Output: Explain the conflict + offer Option A or Option B
```

### Test 4: Conflicting Flags (--tool + --parallel)
```
Input: /create blog-posts --tool qwen --parallel
Expected: error_tool_parallel_conflict()
Output: Explain the conflict + offer Option A or Option B
```

### Test 5: Insufficient Tools for Parallel
```
Input: /create blog-posts --parallel (only 1 tool available)
Expected: error_insufficient_tools_parallel()
Output: How many available + how many needed + /tool-setup suggestion
```

---

**File Status:** Ready for integration into guide-agent's execute_user_command() flow.

**Ownership:** guide-agent (read-only reference, called by guide-agent at runtime)

**Version:** 1.0 (Phase 2a)

---

## Accuracy Failure Classes (Phase 1.3a)

Routing now emits command-quality failures in addition to flag parsing errors:

- `low_confidence_extraction` — output confidence below command threshold.
- `missing_citations` — research output failed citation requirement.
- `partial_scrape` — scrape output is incomplete but recoverable through fallback.
- `blocked_target` — crawler blocked by robots/captcha or anti-bot constraints.
- `timeout` — tool exceeded execution window.

These failures are intended for adaptive fallback and should be logged in `logs/tool-performance.jsonl`.

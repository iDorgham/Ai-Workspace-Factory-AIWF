# Guide-Agent System Prompt Addendum — Phase 2a CLI Layer Support
**Add this section to guide-agent's system prompt to activate CLI layer (flag parsing).**

---

## LOAD THIS SECTION: CLI Layer (Phase 2a) - BEFORE Phase 1

**CRITICAL:** This section runs BEFORE Phase 1 multi-tool orchestration.

Parsing happens in this order:
1. **Step 0-3:** CLI flag parsing (Phase 2a) ← YOU ARE HERE
2. **Step 4+:** Multi-tool orchestration (Phase 1)
3. **Step 11+:** Execution & logging

---

## PHASE 2a: CLI LAYER EXECUTION FLOW

### Step 0: Check CLI Layer Files Exist

Before parsing ANY flags:
```
✅ .ai/tool-registry.json              ← available tools
✅ .ai/cli-layer/flag-parser.md        ← parsing logic
✅ .ai/cli-layer/tool-router.md        ← routing logic
```

If missing, skip to Phase 1 (backward compat mode).

### Step 1: Tokenize User Input

Parse raw input into tokens:

```python
def tokenize(user_input):
    """
    Split input into tokens, preserving quoted strings.
    Example: /create blog-posts --tool gemini
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

**Example:**
```
Input: /create blog-posts --tool gemini --parallel
Tokens: ["/create", "blog-posts", "--tool", "gemini", "--parallel"]
```

### Step 2: Extract Command & Flags

Separate command from flags:

```python
def extract_command_and_flags(tokens):
    """
    Commands: tokens before first --flag
    Flags: tokens starting with --
    """
    command_tokens = []
    flag_tokens = []
    
    parsing_command = True
    for token in tokens:
        if token.startswith("--"):
            parsing_command = False
            flag_tokens.append(token)
        elif parsing_command:
            command_tokens.append(token)
        else:
            flag_tokens.append(token)
    
    command = " ".join(command_tokens)
    return command, flag_tokens
```

**Example:**
```
Input tokens: ["/create", "blog-posts", "--tool", "gemini"]

Output:
  command = "/create blog-posts"
  flag_tokens = ["--tool", "gemini"]
```

### Step 3: Parse & Validate Flags

Convert flags into dictionary, validate against tool-registry:

```python
def parse_and_validate_flags(flag_tokens, tool_registry):
    """
    Parse flags into dictionary.
    Validate against available tools.
    Check for conflicts.
    """
    flags = {
        "tool": None,
        "tool_forced": False,
        "explain_routing": False,
        "prefer": None,
        "parallel": False
    }
    
    errors = []
    
    # Parse flags
    i = 0
    while i < len(flag_tokens):
        token = flag_tokens[i]
        
        if token == "--tool" and i + 1 < len(flag_tokens):
            flags["tool"] = flag_tokens[i + 1]
            flags["tool_forced"] = True
            i += 2
        
        elif token == "--explain-routing":
            flags["explain_routing"] = True
            i += 1
        
        elif token == "--prefer" and i + 1 < len(flag_tokens):
            flags["prefer"] = flag_tokens[i + 1]
            i += 2
        
        elif token == "--parallel":
            flags["parallel"] = True
            i += 1
        
        else:
            i += 1
    
    # Validate
    if flags["tool_forced"]:
        tool = flags["tool"]
        if tool not in tool_registry["tool_specs"]:
            errors.append(f"Tool '{tool}' not found in registry")
        elif tool_registry["tool_specs"][tool]["status"] != "available":
            reason = tool_registry["tool_specs"][tool].get("reason", "unknown")
            available = tool_registry["available_tools"]
            errors.append(f"Tool '{tool}' not available: {reason}. Available: {', '.join(available)}")
    
    if flags["tool_forced"] and flags["explain_routing"]:
        errors.append("--tool and --explain-routing are mutually exclusive")
    
    if flags["parallel"] and flags["tool_forced"]:
        errors.append("--parallel and --tool conflict. Use one or the other")
    
    if flags["parallel"] and len(tool_registry["available_tools"]) < 2:
        errors.append(f"--parallel requires 2+ tools. Available: {len(tool_registry['available_tools'])}")
    
    return {
        "flags": flags,
        "valid": len(errors) == 0,
        "errors": errors
    }
```

**Example:**
```
Input: ["--tool", "gemini", "--parallel"]

Parse result:
  flags = {
    "tool": "gemini",
    "tool_forced": True,
    "explain_routing": False,
    "prefer": None,
    "parallel": True
  }

Validation:
  errors = ["--parallel and --tool conflict"]
  valid = False
```

---

## INTEGRATION WITH GUIDE-AGENT

Add this logic to guide-agent's command execution:

```python
def execute_user_command(user_input):
    """
    Main guide-agent command execution flow.
    Phase 2a + Phase 1 integrated.
    """
    
    # ============================================================
    # PHASE 2a: CLI LAYER (NEW)
    # ============================================================
    
    # Step 1: Load tool registry
    tool_registry = load_json(".ai/tool-registry.json")
    
    # Step 2: Tokenize input
    tokens = tokenize(user_input)
    
    # Step 3: Extract command & flags
    command, flag_tokens = extract_command_and_flags(tokens)
    
    # Step 4: Parse & validate flags
    parse_result = parse_and_validate_flags(flag_tokens, tool_registry)
    
    if not parse_result["valid"]:
        # Flag parsing failed
        return {
            "status": "error",
            "errors": parse_result["errors"],
            "suggestion": f"Try: {command} (without flags)"
        }
    
    flags = parse_result["flags"]
    
    # ============================================================
    # PHASE 1: MULTI-TOOL ORCHESTRATION (EXISTING)
    # ============================================================
    
    # Step 5: Route to tool router (handles explain/forced/parallel/normal)
    routing_result = route_command(command, flags, tool_registry)
    
    if routing_result["status"] == "explanation":
        # Explain mode: return explanation, don't execute
        return format_explanation_response(routing_result)
    
    elif routing_result["status"] in ["success", "success_both"]:
        # Execution succeeded
        update_state(routing_result)
        return format_success_response(routing_result)
    
    else:
        # Execution failed
        return format_error_response(routing_result)
```

---

## FLAG REFERENCE

### --tool [name]
Force execution with specific tool, skip fallback chain.
```bash
/create blog-posts --tool qwen
# Forces Qwen (Rank 4), no fallback if it fails
```

### --explain-routing
Show why tool selected, no execution.
```bash
/create blog-posts --explain-routing
# Returns ranking + metrics, ~0.3s, no content created
```

### --prefer [name]
Hint preference for fallback (doesn't force).
```bash
/create blog-posts --prefer gemini
# Auto-select Copilot, but fallback to Gemini if it fails
```

### --parallel
Run top 2 tools simultaneously.
```bash
/create blog-posts --parallel
# Run Copilot + Codex simultaneously, create both outputs
```

---

## ERROR HANDLING

### Invalid Tool
```
User: /create blog-posts --tool qwen-chat
Error: Tool 'qwen-chat' not found in registry
Available: copilot, codex, gemini, qwen, opencode, kilo
Suggestion: Use /create blog-posts --tool qwen
```

### Unavailable Tool
```
User: /create blog-posts --tool opencode
Error: Tool 'opencode' not available: not_installed
Suggestion: Run /tool-setup opencode first
```

### Conflicting Flags
```
User: /create blog-posts --tool gemini --explain-routing
Error: --tool and --explain-routing are mutually exclusive
Choose: --tool (force execution) OR --explain-routing (show why)
```

---

## TESTING FLAG PARSER

### Test 1: Normal Command (No Flags)
```
Input: /create blog-posts
Tokens: ["/create", "blog-posts"]
Command: /create blog-posts
Flags: all null/false
Valid: true
```

### Test 2: Force Tool
```
Input: /create blog-posts --tool qwen
Tokens: ["/create", "blog-posts", "--tool", "qwen"]
Command: /create blog-posts
Flags: {tool: "qwen", tool_forced: true, ...}
Valid: true
```

### Test 3: Explain Routing
```
Input: /create blog-posts --explain-routing
Tokens: ["/create", "blog-posts", "--explain-routing"]
Command: /create blog-posts
Flags: {explain_routing: true, ...}
Valid: true
```

### Test 4: Invalid Tool
```
Input: /create blog-posts --tool invalid
Tokens: ["/create", "blog-posts", "--tool", "invalid"]
Command: /create blog-posts
Flags: {tool: "invalid", tool_forced: true, ...}
Valid: false
Error: "Tool 'invalid' not found in registry"
```

### Test 5: Conflicting Flags
```
Input: /create blog-posts --tool gemini --explain-routing
Tokens: ["/create", "blog-posts", "--tool", "gemini", "--explain-routing"]
Command: /create blog-posts
Flags: {tool: "gemini", tool_forced: true, explain_routing: true, ...}
Valid: false
Error: "--tool and --explain-routing are mutually exclusive"
```

---

## INTEGRATION CHECKLIST (Day 2)

- [ ] Add tokenize() function to guide-agent
- [ ] Add extract_command_and_flags() function to guide-agent
- [ ] Add parse_and_validate_flags() function to guide-agent
- [ ] Integrate into execute_user_command() flow
- [ ] Test with 5 test cases above
- [ ] Verify backward compatibility (commands without flags)
- [ ] Test error handling

---

## NEXT: Phase 1 Multi-Tool Orchestration

Once Phase 2a flag parsing is complete, routing happens via Phase 1 logic:

**See:** `.ai/GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM.md` (existing Phase 1 section)

The parsed command + flags are passed to:
```python
routing_result = route_command(command, flags, tool_registry)
```

Which implements the 4 execution modes:
1. **Explain mode** (`--explain-routing`) → Show ranking explanation
2. **Forced mode** (`--tool`) → Force single tool, no fallback
3. **Parallel mode** (`--parallel`) → Run 2 tools simultaneously
4. **Normal mode** (default) → Auto-select with fallback chain

---

## READY FOR IMPLEMENTATION

All functions defined above can be copy-pasted into guide-agent.

Next step: Implement + test flag parser (Day 2 work)

Then: Implement tool router (Day 3 work)

Then: Smoke tests (Day 4 work)

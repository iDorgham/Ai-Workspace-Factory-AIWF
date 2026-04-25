# CLI Layer — Tool Router Implementation
**Phase 2a: Routing & Execution**

---

## Overview

After flags are parsed, the tool router decides which tool executes and in what mode.

```
Parsed Input:
{
  "command": "/create blog-posts",
  "flags": {
    "tool": "gemini",
    "tool_forced": true,
    "explain_routing": false,
    "prefer": null,
    "parallel": false
  }
}
     ↓
Tool Router
     ↓
Decision: Execute with Gemini (forced), skip fallback
     ↓
Load: .ai/tool-adapters/gemini_adapter.md
Execute: Gemini CLI
```

---

## Routing Decision Tree

### Top Level: Branch by Flag Priority

```python
def route_command(command, flags, tool_registry):
    """
    Main routing function.
    Branches based on flag priority.
    """
    
    # Priority 1: --explain-routing (no execution)
    if flags["explain_routing"]:
        return explain_routing_mode(command, tool_registry)
    
    # Priority 2: --tool (forced single tool)
    if flags["tool_forced"]:
        return forced_tool_mode(command, flags["tool"], tool_registry)
    
    # Priority 3: --parallel (dual tools)
    if flags["parallel"]:
        return parallel_execution_mode(command, tool_registry)
    
    # Default: Normal mode with optional --prefer
    return normal_execution_mode(command, flags.get("prefer"), tool_registry)
```

---

## Mode 1: Explain Routing Mode

**Purpose:** Show why a tool would be selected (no execution)

**Execution:**
```python
def explain_routing_mode(command, tool_registry):
    """
    Show tool ranking + metrics without executing.
    """
    
    # Step 1: Parse command type
    command_type = parse_command_type(command)
    # e.g., "/create blog-posts" → command_type = "create_blog_posts"
    
    # Step 2: Load command routing rules
    command_routing = load_json(".ai/commands_multi_tool.md")
    preferred_ranking = command_routing.get(command_type, [])
    
    # Step 3: Filter to available tools only
    available_tools = tool_registry["available_tools"]
    actual_ranking = [t for t in preferred_ranking if t in available_tools]
    
    # Step 4: Get performance metrics
    performance_log = load_jsonl(".ai/logs/tool-performance.jsonl")
    tool_metrics = aggregate_metrics_by_tool(performance_log, command_type)
    
    # Step 5: Build explanation
    explanation = {
        "command": command,
        "ranking": []
    }
    
    for rank, tool in enumerate(actual_ranking, 1):
        metrics = tool_metrics.get(tool, {})
        
        explanation["ranking"].append({
            "rank": rank,
            "tool": tool,
            "latency_ms": metrics.get("avg_latency_ms", "unknown"),
            "cost_usd": metrics.get("avg_cost_usd", "unknown"),
            "success_rate": metrics.get("success_rate", "unknown"),
            "why_this_rank": get_rank_explanation(tool, command_type)
        })
    
    explanation["selected_tool"] = actual_ranking[0] if actual_ranking else None
    explanation["available_tools"] = available_tools
    
    # Step 6: Return explanation (no logging, no execution)
    return {
        "status": "explanation",
        "data": explanation,
        "timestamp": get_timestamp()
    }
```

**Response format:**
```
🧭 Tool Selection for /create blog-posts

Ranking & Performance:
  Rank 1: Copilot
    ├─ Latency: 3.5s (avg 20 runs)
    ├─ Cost: $0.003 per command
    ├─ Success: 97%
    └─ Why: Content quality matters most, Copilot is strong here

  Rank 2: Codex
    ├─ Latency: 2.5s (avg 18 runs)
    ├─ Cost: $0.002 per command
    ├─ Success: 96%
    └─ Why: Cheaper, fast fallback, nearly same quality

  Rank 3: Gemini
    ├─ Latency: 3.1s
    ├─ Cost: $0.075 per command
    ├─ Success: 96%
    └─ Why: Large context, multimodal, pricier

Selected: Copilot (Rank 1)

Available tools: copilot, codex, gemini, qwen

Override with:
  /create blog-posts --tool codex (force Codex)
  /create blog-posts --prefer qwen (prefer Qwen if Copilot fails)
  /create blog-posts --parallel (get both Copilot + Codex)
```

---

## Mode 2: Forced Tool Mode

**Purpose:** Force execution with specific tool, skip fallback

**Execution:**
```python
def forced_tool_mode(command, forced_tool, tool_registry):
    """
    Execute with forced tool.
    If tool fails, error (no fallback).
    """
    
    # Step 1: Load tool adapter
    adapter_file = tool_registry["tool_specs"][forced_tool]["adapter_file"]
    tool_adapter = load_markdown(adapter_file)
    
    # Step 2: Load tool-specific state
    state_file = f".ai/memory/multi-tool-state/{forced_tool}.session.json"
    tool_state = load_json(state_file)
    
    # Step 3: Check token budget
    context_window = tool_registry["tool_specs"][forced_tool]["context_window"]
    tokens_available = context_window - tool_state["tokens_used_this_session"]
    
    if tokens_available < 10000:
        return {
            "status": "error",
            "message": f"Insufficient tokens in {forced_tool} session",
            "tokens_available": tokens_available,
            "suggestion": f"Reset session or use different tool"
        }
    
    # Step 4: Execute command
    execution_result = execute_tool(
        tool=forced_tool,
        command=command,
        adapter=tool_adapter,
        state=tool_state
    )
    
    # Step 5: Check result
    if execution_result["status"] == "success":
        # Success - update state and return
        update_state(forced_tool, execution_result)
        return {
            "status": "success",
            "tool": forced_tool,
            "tool_forced": True,
            "output": execution_result["output"]
        }
    
    else:
        # Failure - NO fallback (forced tool)
        log_command(command, forced_tool, "failed", reason="forced_tool_failed")
        return {
            "status": "error",
            "message": f"Forced tool '{forced_tool}' failed",
            "error": execution_result["error"],
            "suggestion": f"Use /create blog-posts --tool [other] to try different tool"
        }
```

**Error response:**
```
❌ Forced tool failed: gemini
Error: Timeout (>300s)

Since --tool was specified, no fallback chain.

Options:
  • Retry: /create blog-posts --tool gemini
  • Different tool: /create blog-posts --tool copilot
  • Let system decide: /create blog-posts
  • See why: /create blog-posts --explain-routing
```

---

## Mode 3: Parallel Execution Mode

**Purpose:** Run top 2 tools simultaneously, create both outputs

**Execution:**
```python
def parallel_execution_mode(command, tool_registry):
    """
    Execute Rank 1 + Rank 2 tools concurrently.
    """
    
    # Step 1: Get top 2 available tools
    command_type = parse_command_type(command)
    command_routing = load_json(".ai/commands_multi_tool.md")
    preferred_ranking = command_routing.get(command_type, [])
    available_tools = tool_registry["available_tools"]
    actual_ranking = [t for t in preferred_ranking if t in available_tools]
    
    if len(actual_ranking) < 2:
        return {
            "status": "error",
            "message": "Parallel execution requires at least 2 available tools",
            "available": len(actual_ranking)
        }
    
    rank_1_tool = actual_ranking[0]
    rank_2_tool = actual_ranking[1]
    
    # Step 2: Load both adapters
    adapter_1 = load_markdown(
        tool_registry["tool_specs"][rank_1_tool]["adapter_file"]
    )
    adapter_2 = load_markdown(
        tool_registry["tool_specs"][rank_2_tool]["adapter_file"]
    )
    
    # Step 3: Start both executions concurrently
    import threading
    
    result_1 = {}
    result_2 = {}
    
    def execute_tool_1():
        result_1.update(execute_tool(rank_1_tool, command, adapter_1))
    
    def execute_tool_2():
        result_2.update(execute_tool(rank_2_tool, command, adapter_2))
    
    thread_1 = threading.Thread(target=execute_tool_1)
    thread_2 = threading.Thread(target=execute_tool_2)
    
    thread_1.start()
    thread_2.start()
    
    # Step 4: Wait for both to complete
    thread_1.join(timeout=300)  # Max 300s
    thread_2.join(timeout=300)
    
    # Step 5: Process results
    results = {
        "status": "parallel_complete",
        "execution_mode": "parallel",
        "tools": [rank_1_tool, rank_2_tool],
        "outputs": {}
    }
    
    if result_1.get("status") == "success":
        results["outputs"][rank_1_tool] = result_1["output"]
        update_state(rank_1_tool, result_1)
    else:
        results[rank_1_tool + "_error"] = result_1.get("error")
    
    if result_2.get("status") == "success":
        results["outputs"][rank_2_tool] = result_2["output"]
        update_state(rank_2_tool, result_2)
    else:
        results[rank_2_tool + "_error"] = result_2.get("error")
    
    # Step 6: Return comparison
    return {
        "status": "success_both" if len(results["outputs"]) == 2 else "partial",
        "data": results,
        "comparison": format_parallel_comparison(results)
    }
```

**Response:**
```
✅ Parallel execution complete

Generated with:
  ✓ Copilot (3.5s, $0.003)
  ✓ Codex (2.5s, $0.002)

Created:
  content/sovereign/blog-posts/[slug]_[tool]_v[version].md
  content/sovereign/blog-posts/[slug]_[tool]_v[version].md

Quality Scores:
  Copilot: Brand Voice 94% | Originality 97%
  Codex: Brand Voice 91% | Originality 96%

Recommendation: Both are good. Copilot has slightly higher quality.

Choose which to keep:
  /keep copilot
  /keep codex
  /compare
```

---

## Mode 4: Normal Execution Mode (with Optional Prefer)

**Purpose:** Auto-select best tool, fallback chain with optional preference

**Execution:**
```python
def normal_execution_mode(command, preferred_tool=None, tool_registry=None):
    """
    Normal execution with adaptive fallback.
    """
    
    # Step 1: Get ranking
    command_type = parse_command_type(command)
    command_routing = load_json(".ai/commands_multi_tool.md")
    preferred_ranking = command_routing.get(command_type, [])
    available_tools = tool_registry["available_tools"]
    actual_ranking = [t for t in preferred_ranking if t in available_tools]
    
    if not actual_ranking:
        return {
            "status": "error",
            "message": "No tools available for this command"
        }
    
    # Step 2: Execute Rank 1
    rank_1_tool = actual_ranking[0]
    result = execute_tool(rank_1_tool, command, tool_registry)
    
    if result["status"] == "success":
        # Success!
        update_state(rank_1_tool, result)
        log_command(command, rank_1_tool, "success", tool_rank=1)
        return result
    
    # Step 3: Rank 1 failed - check preference
    if preferred_tool and preferred_tool in available_tools:
        # User has preference - try that
        result = execute_tool(preferred_tool, command, tool_registry)
        
        if result["status"] == "success":
            update_state(preferred_tool, result)
            log_command(command, preferred_tool, "success", 
                       tool_rank=999, fallback_from=rank_1_tool,
                       fallback_reason="user_preference")
            return result
        
        else:
            # Preference also failed - error
            log_command(command, preferred_tool, "failed", 
                       fallback_from=rank_1_tool)
            return {
                "status": "error",
                "message": f"Both {rank_1_tool} and {preferred_tool} failed"
            }
    
    # Step 4: No preference - try Rank 2
    if len(actual_ranking) > 1:
        rank_2_tool = actual_ranking[1]
        result = execute_tool(rank_2_tool, command, tool_registry)
        
        if result["status"] == "success":
            update_state(rank_2_tool, result)
            log_command(command, rank_2_tool, "success", 
                       tool_rank=2, fallback_from=rank_1_tool)
            return result
    
    # Step 5: Try Rank 3
    if len(actual_ranking) > 2:
        rank_3_tool = actual_ranking[2]
        result = execute_tool(rank_3_tool, command, tool_registry)
        
        if result["status"] == "success":
            update_state(rank_3_tool, result)
            log_command(command, rank_3_tool, "success", tool_rank=3)
            return result
    
    # Step 6: All failed
    return {
        "status": "error",
        "message": f"All {len(actual_ranking)} available tools failed",
        "tools_tried": actual_ranking,
        "suggestion": "Check logs for details or try with --tool to force specific tool"
    }
```

---

## Integration with Guide-Agent

```python
def guide_agent_execute(user_input):
    """Main execution flow in guide-agent"""
    
    # Load registries
    tool_registry = load_json(".ai/tool-registry.json")
    
    # Parse flags
    parse_result = parse_cli_input(user_input, tool_registry)
    
    if not parse_result["valid"]:
        return error_response(parse_result["errors"])
    
    command = parse_result["command"]
    flags = parse_result["flags"]
    
    # Route to handler
    routing_result = route_command(command, flags, tool_registry)
    
    # Return response to user
    if routing_result["status"] in ["success", "success_both"]:
        return format_success_response(routing_result)
    elif routing_result["status"] == "explanation":
        return format_explanation_response(routing_result)
    else:
        return format_error_response(routing_result)
```

---

## Logging Integration

All routing decisions are logged:

```python
def log_command(command, tool, status, **extra_fields):
    """Log command execution"""
    
    entry = {
        "timestamp": get_timestamp(),
        "command": command,
        "tool": tool,
        "status": status,
        **extra_fields
    }
    
    # Append to workflow log
    append_jsonl(".ai/logs/workflow.jsonl", entry)
    
    # Append to tool-specific performance log
    append_jsonl(".ai/logs/tool-performance.jsonl", {
        "timestamp": entry["timestamp"],
        "tool": tool,
        "command": command,
        "status": status,
        **extra_fields
    })
```

---

## Next: Tool Adapters

Once routing decides which tool to use, the appropriate adapter (copilot_adapter.md, codex_adapter.md, etc.) is loaded and executed.

---

## Accuracy-First Update (Phase 1.3a)

- Canonical routing source is `.ai/cli-layer/command-routing.json`.
- Research/scrape command variants resolve from schema `patterns` instead of ad-hoc string parsing.
- Quality gates are enforced per command via schema `quality_gates`:
  - `min_confidence`
  - `require_citations`
  - `allow_partial_results`
- Explain mode returns `routing_rule_id` and deterministic ranking rationale.
- Failure taxonomy used by fallback logic:
  - `timeout`
  - `blocked_target`
  - `partial_scrape`
  - `low_confidence_extraction`
  - `missing_citations`

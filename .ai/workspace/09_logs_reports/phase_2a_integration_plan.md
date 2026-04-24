# Phase 2a: CLI Layer Integration Plan
**Wiring CLI layer into guide-agent**

---

## Integration Strategy

```
BEFORE (Phase 1):
  CLAUDE.md (startup) → Load state → Execute command → Log
  
AFTER (Phase 2a):
  CLAUDE.md (startup) → Load CLI files → Parse flags → Route → Execute → Log
                                    ↑ NEW
```

---

## Files to Update

### 1. CLAUDE.md (Startup Sequence)
**Current Step 1.5:** Load multi-tool files
**New Step 1.6:** Load CLI layer files

Add after Step 1.5:
```markdown
### Step 1.6 — Load CLI layer files (Phase 2a)
```
READ: .ai/tool-registry.json           ← available tools
READ: .ai/cli-layer/flag_parser.md    ← flag parsing logic
READ: .ai/cli-layer/tool_router.md    ← routing logic
```
```

### 2. Guide-Agent System Prompt (New Section)
**File:** `.ai/GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM.md`

**Add new section:** "CLI LAYER EXECUTION FLOW (Phase 2a)"

Steps:
```
Step 11: Parse CLI flags (before routing)
Step 12: Validate flags against tool-registry
Step 13: Route to execution mode (explain/forced/parallel/normal)
Step 14: Execute selected tool(s)
Step 15: Update per-tool state
```

### 3. Commands Router (Update)
**File:** `.ai/commands_multi_tool.md`

Add 6-tool rankings for each command type:
```
/create blog-posts:
  Rank 1: copilot
  Rank 2: codex
  Rank 3: gemini
  Rank 4: qwen
  Rank 5: opencode
  Rank 6: kilo
```

### 4. Data Ownership (Update)
**File:** `.ai/data_ownership_multi_tool.md`

Add 6 new tool output patterns:
```
content/sovereign/blog-posts/[slug]_[tool]_v[version].md (copilot output)
content/sovereign/blog-posts/[slug]_[tool]_v[version].md (codex output)
... (for all 6 tools)
```

---

## Integration Execution Plan

### Day 1: Core Updates

- [ ] Update CLAUDE.md Step 1.6 (load CLI files)
- [ ] Update session summary to show CLI layer active
- [ ] Verify all tool-registry fields present
- [ ] Test tool-registry.json parsing

### Day 2: Guide-Agent Integration

- [ ] Add CLI parsing to guide-agent startup
- [ ] Implement flag parser logic in guide-agent
- [ ] Implement tool router logic in guide-agent
- [ ] Create/update helper functions for:
  - `parse_cli_input(user_input, tool_registry)`
  - `route_command(command, flags, tool_registry)`
  - `validate_flags(flags, tool_registry)`

### Day 3: Commands & Routing

- [ ] Update commands_multi_tool.md with 6-tool rankings
- [ ] Update data-ownership rules for 6 tool outputs
- [ ] Update logging format to include tool metadata
- [ ] Create error response templates

### Day 4: Testing

- [ ] Test 1: Normal execution (auto-select)
- [ ] Test 2: Forced tool
- [ ] Test 3: Explain routing
- [ ] Test 4: Parallel mode
- [ ] Test 5: Fallback chain

---

## Code Integration Points

### Point 1: Flag Parsing (in guide-agent)

```python
# After Step 2 (load state), add:

# NEW: Parse CLI flags
tool_registry = load_json(".ai/tool-registry.json")
parse_result = parse_cli_input(user_input, tool_registry)

if not parse_result["valid"]:
    return error_response(parse_result["errors"])

command = parse_result["command"]
flags = parse_result["flags"]
```

### Point 2: Tool Routing (replace old routing)

```python
# OLD:
selected_tool = "claude"  # hardcoded

# NEW:
routing_result = route_command(command, flags, tool_registry)

if routing_result["status"] == "explanation":
    return format_explanation(routing_result)
elif routing_result["status"] == "error":
    return format_error(routing_result)
else:
    selected_tool = routing_result["tool"]
    execute_result = routing_result["data"]
```

### Point 3: State Updates (add per-tool tracking)

```python
# OLD:
state["last_tool"] = "claude"

# NEW:
state["last_tool"] = selected_tool
state["last_tool_forced"] = flags.get("tool_forced", False)
state["last_execution_mode"] = routing_result.get("execution_mode", "normal")

# Also update tool-specific state
tool_state_file = f".ai/memory/multi-tool-state/{selected_tool}.session.json"
update_tool_state(tool_state_file, execute_result)
```

---

## Validation Checklist

### Before Integration
- [ ] All 10 core CLI files created
- [ ] All 7 tool adapters created
- [ ] Tool registry populated
- [ ] Flag parser logic complete
- [ ] Tool router logic complete

### During Integration
- [ ] CLAUDE.md updated (Step 1.6)
- [ ] Guide-agent startup updated
- [ ] Flag parsing integrated
- [ ] Tool routing integrated
- [ ] State updates working

### After Integration
- [ ] Tool registry loads correctly
- [ ] Flags parse without errors
- [ ] Tools route correctly per command
- [ ] Fallback chains work
- [ ] State updates apply
- [ ] Logging captures tool metadata

---

## Success Criteria

✅ **Phase 2a Integration Success:**

1. **Flag Parsing Works**
   ```bash
   /create blog-posts --tool qwen
   → Parses successfully
   → Validates qwen is available
   → Returns parsed structure
   ```

2. **Tool Routing Works**
   ```bash
   /create blog-posts
   → Auto-selects Copilot (Rank 1)
   → Executes and returns content
   → Logs with tool=copilot
   ```

3. **Explain Routing Works**
   ```bash
   /create blog-posts --explain-routing
   → Returns ranking explanation
   → Shows performance metrics
   → No content created
   ```

4. **Parallel Mode Works**
   ```bash
   /create blog-posts --parallel
   → Runs Copilot + Codex simultaneously
   → Creates both outputs
   → Returns comparison
   ```

5. **Fallback Chain Works**
   ```bash
   /create blog-posts (with Copilot timeout)
   → Copilot times out
   → Fallback to Codex
   → Codex succeeds
   → Output saved as codex version
   ```

6. **State Management Works**
   - Per-tool session files update
   - Global state reflects last_tool
   - Logs capture all metadata
   - Cost tracking accurate

---

## Rollback Plan

If integration fails, can rollback to Phase 1:

```bash
# Step 1: Comment out CLI layer loading in CLAUDE.md
# Step 2: Revert to old commands.md (archived in .ai/archive/)
# Step 3: Stop parsing flags (use simple command routing)
# Step 4: All Phase 1 functionality restored
```

**Rollback time:** < 5 minutes  
**Data loss:** None (all files preserved)

---

## Timeline

- **Day 1:** Update startup files (CLAUDE.md, guide-agent)
- **Day 2:** Integrate flag parser + tool router
- **Day 3:** Update commands + data ownership
- **Day 4:** Run smoke tests (5 scenarios)
- **Day 5:** Fix any issues, refine
- **Day 6:** Performance optimization
- **Day 7:** Final validation + monitoring setup

**Total:** ~1 week for full integration + testing

---

## Next: Begin Integration

Ready to start Day 1 integration work?

- `start-day-1` → Update CLAUDE.md and startup sequence
- `review` → Review integration plan before proceeding
- `questions` → Ask clarifying questions

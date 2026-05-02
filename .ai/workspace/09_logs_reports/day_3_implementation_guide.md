# Day 3 Implementation Guide — Phase 1 Tool-Router

**Date:** 2026-04-13  
**Status:** Ready for Execution  
**Objective:** Implement tool-router for Phase 1 multi-tool orchestration

---

## Day 3 Overview

Today we integrate Phase 2a flag parsing with Phase 1 multi-tool routing. The tool-router decides which tool executes based on:
- Command type (what's being asked)
- Flags (user preferences from Phase 2a)
- Tool availability (which tools are installed)
- Performance metrics (speed, cost, quality)

---

## Execution Flow (Recap)

```
User Input: "/create blog-posts --tool qwen"
  ↓
Phase 2a (Done): Tokenize → Extract → Parse → Validate Flags
  Result: {command: "/create blog-posts", flags: {tool: "qwen", tool_forced: true, ...}}
  ↓
Phase 1 (Today): Route Command → Select Tool → Execute
  Decision: Use Qwen (forced), skip fallback
  ↓
Output: Content + Logs
```

---

## 4 Execution Modes to Implement

### 1. Normal Mode
**Trigger:** No flags (default behavior)  
**Behavior:** Auto-select Rank 1, fallback chain enabled

```
Try Rank 1 Tool
  ↓ (if fails) ↓
Try Rank 2 Tool (or user's --prefer if set)
  ↓ (if fails) ↓
Try Rank 3 Tool
  ↓ (if fails) ↓
Error: All tools failed
```

### 2. Explain Mode
**Trigger:** `--explain-routing` flag  
**Behavior:** Show ranking explanation, NO execution

```
Show:
  - Rank 1, 2, 3 tools
  - Why each rank (optimization strategy)
  - Performance metrics (latency, cost, success rate)
  - Selected tool (Rank 1)
  - Available tools list

Return: Explanation object (no tool execution)
```

### 3. Forced Mode
**Trigger:** `--tool [name]` flag  
**Behavior:** Execute specific tool, NO fallback

```
Execute Forced Tool
  ↓ (if success) ↓
Return success
  ↓ (if fails) ↓
Error: No fallback chain (user forced this tool)
```

### 4. Parallel Mode
**Trigger:** `--parallel` flag  
**Behavior:** Run Rank 1 + Rank 2 simultaneously

```
Start Thread 1: Execute Rank 1 Tool
Start Thread 2: Execute Rank 2 Tool
  ↓
Wait for both to complete (max 300s each)
  ↓
Return both outputs + comparison
```

---

## Implementation Tasks (Sequential)

### Task 1: Create Tool-Router Module
**Time:** ~40 min  
**Input:** `.ai/cli-layer/tool_router.md` (pseudocode)  
**Output:** `.ai/scripts/tool-router.py` (executable module)

**Subtasks:**
1. [ ] Create `.ai/scripts/tool-router.py`
2. [ ] Implement `route_command()` main function
3. [ ] Implement `explain_routing_mode()`
4. [ ] Implement `forced_tool_mode()`
5. [ ] Implement `parallel_execution_mode()`
6. [ ] Implement `normal_execution_mode()`
7. [ ] Add helper functions:
   - `parse_command_type()` — Extract command type from input
   - `load_command_routing()` — Load tool ranking rules
   - `get_available_tools()` — Filter by availability
   - `execute_tool()` — Mock tool execution
   - `update_state()` — Update tool session state
   - `log_command()` — Log execution to workflow.jsonl

**Testing:** Can unit-test each mode independently

---

### Task 2: Create Command Routing Rules
**Time:** ~15 min  
**Input:** Tool registry + existing command system  
**Output:** `.ai/commands/commands.md` (tool rankings per command)

**Content:** Mapping of commands to tool rankings
```json
{
  "create_blog_posts": ["copilot", "codex", "gemini", "qwen"],
  "optimize_images": ["gemini", "codex", "copilot"],
  "extract_brand_voice": ["copilot", "gemini"],
  ...
}
```

**Why:** Routes decisions based on command type + tool strengths

---

### Task 3: Create Day 3 Test Suite
**Time:** ~30 min  
**Input:** 4 execution modes + edge cases  
**Output:** `tests/day-3-tool-router-tests.json` (12 test cases)

**Test Coverage:**
- Normal Mode: 3 tests
  - Rank 1 succeeds
  - Rank 1 fails, Rank 2 succeeds
  - All ranks fail
- Explain Mode: 2 tests
  - Show ranking
  - With performance metrics
- Forced Mode: 3 tests
  - Forced tool succeeds
  - Forced tool fails (no fallback)
  - Forced tool unavailable (error)
- Parallel Mode: 3 tests
  - Both tools succeed
  - One tool fails, one succeeds
  - Both fail

**Total:** 12 comprehensive test cases

---

### Task 4: Create Test Runner
**Time:** ~25 min  
**Input:** Tool-router module + test suite  
**Output:** `.ai/scripts/test-tool-router.py` (executable)

**Features:**
- Load test cases from JSON
- Execute each routing mode
- Compare results vs expected
- Generate pass/fail summary
- Save results to logs

---

### Task 5: Run Full Test Suite
**Time:** ~10 min  
**Input:** Tool-router + tests  
**Output:** `logs/day-[day]-[report]-results.json` (12/12 PASS?)

**Actions:**
1. [ ] Run: `python3 .ai/scripts/test-tool-router.py`
2. [ ] Verify: All 12 tests pass
3. [ ] Check: tool-performance.jsonl created with metrics
4. [ ] Check: workflow.jsonl populated with logs

---

### Task 6: Integration Verification
**Time:** ~10 min  
**Input:** Phase 2a + Phase 1 together  
**Output:** `.ai/INTEGRATION_VERIFICATION.md` (go/no-go check)

**Verification:**
- [ ] Phase 2a flag parsing works
- [ ] Phase 1 tool routing works
- [ ] Integration flow: Phase 2a → Phase 1 → Execute
- [ ] Logging working (workflow.jsonl, tool-performance.jsonl)
- [ ] State management working (.ai/memory/multi-tool-state/)
- [ ] Error handling integrated

---

### Task 7: Create Day 3 Completion Report
**Time:** ~10 min  
**Input:** All test results + integration checks  
**Output:** `logs/day-[day]-[report].md` (summary)

**Includes:**
- Test results (12/12 PASS rate)
- Integration status
- Files created/modified
- Known issues (if any)
- Handoff to Day 4 (smoke tests)

---

## Files to Create/Modify

### New Files
- [ ] `.ai/scripts/tool-router.py` (350+ lines)
- [ ] `.ai/commands/commands.md` (command → tool rankings)
- [ ] `tests/day-3-tool-router-tests.json` (12 test cases)
- [ ] `.ai/scripts/test-tool-router.py` (400+ lines)
- [ ] `logs/day-[day]-[report]-results.json` (generated)
- [ ] `logs/day-[day]-[report].md` (summary)
- [ ] `.ai/INTEGRATION_VERIFICATION.md` (checklist)

### Modified Files
- [ ] `.ai/memory/state.json` (add Day 3 status)
- [ ] `CLAUDE.md` (update version to 3.2.0-Phase1.3)

---

## Code Structure (tool-router.py)

```python
# Tool Router Module

import json
import threading
from datetime import datetime

class ToolRouter:
    def __init__(self, tool_registry, command_routing):
        self.tool_registry = tool_registry
        self.command_routing = command_routing
    
    def route_command(self, command, flags):
        """Main routing decision."""
        if flags["explain_routing"]:
            return self.explain_routing_mode(command)
        elif flags["tool_forced"]:
            return self.forced_tool_mode(command, flags["tool"])
        elif flags["parallel"]:
            return self.parallel_execution_mode(command)
        else:
            return self.normal_execution_mode(command, flags.get("prefer"))
    
    def explain_routing_mode(self, command):
        """Show tool ranking explanation."""
        # ... implementation ...
    
    def forced_tool_mode(self, command, forced_tool):
        """Execute with forced tool."""
        # ... implementation ...
    
    def parallel_execution_mode(self, command):
        """Execute Rank 1 + Rank 2 simultaneously."""
        # ... implementation ...
    
    def normal_execution_mode(self, command, preferred_tool):
        """Auto-select Rank 1, fallback chain."""
        # ... implementation ...
```

---

## Testing Strategy

### Unit Tests
- Each mode independently
- Edge cases (tool unavailable, no tools available)
- Error handling

### Integration Tests
- Phase 2a → Phase 1 flow
- Flag parsing → routing decision
- Logging integration

### Performance Tests
- Fallback chain speed
- Parallel execution timing
- State management overhead

---

## Success Criteria (Day 3)

✅ All 4 execution modes working  
✅ All 12 test cases passing  
✅ Command routing rules defined  
✅ Integration verified (Phase 2a + Phase 1)  
✅ Logging working (workflow.jsonl, tool-performance.jsonl)  
✅ State management integrated  
✅ Documentation complete  

---

## Time Budget

| Task | Time | Cumulative |
|------|------|-----------|
| Tool-Router Module | 40 min | 40 min |
| Command Routing Rules | 15 min | 55 min |
| Test Suite Creation | 30 min | 85 min |
| Test Runner | 25 min | 110 min |
| Run Tests | 10 min | 120 min |
| Integration Verify | 10 min | 130 min |
| Completion Report | 10 min | 140 min |

**Total: ~140 minutes** (plus debugging if needed)

---

## Expected Outcomes

### After Task 1
✅ Tool routing logic complete  
✅ All modes callable  
✅ Helper functions ready  

### After Task 2
✅ Command routing rules defined  
✅ Tool strengths mapped  
✅ Ranking strategy clear  

### After Task 3
✅ 12 test cases prepared  
✅ Edge cases covered  
✅ Mode combinations tested  

### After Task 4
✅ Test runner executable  
✅ Can re-run tests anytime  
✅ Results exportable  

### After Task 5
✅ 12/12 tests passing  
✅ Performance metrics logged  
✅ Execution flow verified  

### After Task 6
✅ Integration verified  
✅ All components connected  
✅ Ready for Day 4  

### After Task 7
✅ Complete documentation  
✅ Handoff to Day 4  
✅ Day 3 summary archived  

---

## Rollback Plan

If major issues:
1. Check tool registry validity
2. Verify command routing rules
3. Test individual modes in isolation
4. Check logging infrastructure
5. Restore v3.2 files if needed (in `.ai/archive/`)

---

## Next Checkpoint

**After Day 3:** Tool-router is fully functional + tested  
**Day 4:** Smoke tests (actual commands via CLI flags)  
**Days 5-7:** Refinement + optimization

---

**Document Status:** Ready for Day 3 execution  
**Last Updated:** 2026-04-13  
**Version:** 1.0  
**Owner:** guide-agent

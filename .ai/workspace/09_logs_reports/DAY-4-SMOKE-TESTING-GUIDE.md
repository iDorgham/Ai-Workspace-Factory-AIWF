# Day 4 Smoke Testing Guide — End-to-End Integration

**Date:** 2026-04-13  
**Status:** Ready for Execution  
**Objective:** Run end-to-end smoke tests verifying Phase 2a + Phase 1 integration

---

## Day 4 Overview

Today we run smoke tests that exercise the complete system:
1. User input with CLI flags (Phase 2a requirement)
2. Flag parsing and validation (Phase 2a)
3. Tool selection decision (Phase 1)
4. Tool execution (Phase 1)
5. Logging (both phases)

**Success Criteria:** 10/10 smoke tests pass, all logs generated correctly.

---

## What Smoke Tests Validate

### Phase 2a Integration
- ✅ Flag tokenization works
- ✅ Flag extraction works
- ✅ Flag parsing works
- ✅ Flag validation works
- ✅ Error handling for invalid flags

### Phase 1 Integration
- ✅ Command type parsing works
- ✅ Tool ranking lookup works
- ✅ Tool execution works
- ✅ Fallback chain works
- ✅ Logging works

### End-to-End Flow
- ✅ Phase 2a → Phase 1 → Execution
- ✅ User input → Output + Logs
- ✅ All error paths handled

---

## 10 Smoke Test Cases

### Test 1: Normal Mode (Rank 1 Succeeds)
```bash
Input: /create blog-posts
Expected: Copilot executes, output generated
Validate: workflow.jsonl has entry with tool=copilot, status=success
```

### Test 2: Forced Mode (--tool qwen)
```bash
Input: /create blog-posts --tool qwen
Expected: Qwen executes (forced), skip fallback
Validate: workflow.jsonl has entry with tool=qwen, tool_forced=true
```

### Test 3: Explain Mode (--explain-routing)
```bash
Input: /create blog-posts --explain-routing
Expected: Show ranking, no execution, <500ms latency
Validate: Return object has status=explanation, no output generated
```

### Test 4: Parallel Mode (--parallel)
```bash
Input: /create blog-posts --parallel
Expected: Copilot + Codex execute simultaneously
Validate: workflow.jsonl has 2 entries (copilot + codex)
```

### Test 5: Prefer Mode (--prefer gemini)
```bash
Input: /create blog-posts --prefer gemini
Expected: Try Copilot (Rank 1), if fails try Gemini (preferred)
Validate: workflow.jsonl shows fallback with fallback_reason=user_preference
```

### Test 6: Invalid Tool (--tool invalid)
```bash
Input: /create blog-posts --tool invalid
Expected: Error, suggest available tools
Validate: Error object has error_type=invalid_tool
```

### Test 7: Unavailable Tool (--tool opencode if not installed)
```bash
Input: /create blog-posts --tool opencode
Expected: Error, suggest /tool-setup
Validate: Error object has error_type=tool_unavailable
```

### Test 8: Conflicting Flags (--tool X --explain-routing)
```bash
Input: /create blog-posts --tool gemini --explain-routing
Expected: Error, explain conflict
Validate: Error object has error_type=conflicting_flags
```

### Test 9: Image Optimization (Gemini-heavy command)
```bash
Input: /optimize images
Expected: Gemini selected (Rank 1 for this command)
Validate: workflow.jsonl has tool=gemini
```

### Test 10: Bulk Operation (Speed-optimized)
```bash
Input: /export
Expected: Qwen selected (Rank 1 for this command)
Validate: workflow.jsonl has tool=qwen
```

---

## Smoke Test Execution Plan

### Phase 1: Setup
**Time:** ~5 min

```bash
# Verify all files exist
ls -la .ai/scripts/tool-router.py
ls -la .ai/commands_multi_tool.md
ls -la tests/day-3-tool-router-tests.json

# Verify Phase 2a still working
python3 .ai/scripts/test-flag-parser.py --quick  # Should still pass
```

### Phase 2: Create Smoke Test Suite
**Time:** ~20 min

Create `tests/day-4-smoke-tests.json` with 10 test cases

---

### Phase 3: Create Smoke Test Runner
**Time:** ~30 min

Create `.ai/scripts/run-smoke-tests.py`:
- Load smoke test cases
- Execute each test
- Capture output + logs
- Validate results
- Generate report

---

### Phase 4: Execute Smoke Tests
**Time:** ~15 min

```bash
python3 .ai/scripts/run-smoke-tests.py --verbose
# Expected: 10/10 PASS
```

---

### Phase 5: Verify Logs
**Time:** ~10 min

```bash
# Check workflow.jsonl
tail -20 logs/workflow.jsonl | python3 -m json.tool

# Check tool-performance.jsonl
tail -20 logs/tool-performance.jsonl | python3 -m json.tool

# Count entries
wc -l logs/workflow.jsonl
wc -l logs/tool-performance.jsonl
```

---

### Phase 6: Integration Verification
**Time:** ~10 min

**Checklist:**
- ✅ Phase 2a flag parsing working
- ✅ Phase 1 tool routing working
- ✅ Both phases integrated
- ✅ Logs generated correctly
- ✅ All error paths tested
- ✅ All success paths tested

---

### Phase 7: Create Completion Report
**Time:** ~15 min

Create `logs/day-[day]-[report].md`:
- Test results (10/10 PASS rate)
- Log verification
- Integration status
- Known issues (if any)
- Readiness assessment for production

---

## Expected Outcomes

### After Execution
- ✅ 10/10 smoke tests passing
- ✅ workflow.jsonl populated with 10+ entries
- ✅ tool-performance.jsonl populated with metrics
- ✅ All CLI flags working
- ✅ All error paths handled
- ✅ All execution modes verified

### Log Examples

**workflow.jsonl entry (success):**
```json
{
  "timestamp": "2026-04-13T08:00:00.123456",
  "command": "/create blog-posts",
  "tool": "copilot",
  "status": "success",
  "mode": "normal",
  "tool_rank": 1,
  "fallback_used": false,
  "output_tokens": 2500
}
```

**workflow.jsonl entry (error):**
```json
{
  "timestamp": "2026-04-13T08:05:00.654321",
  "command": "/create blog-posts --tool invalid",
  "tool": null,
  "status": "error",
  "error_type": "invalid_tool",
  "message": "Tool 'invalid' not found in registry",
  "available_tools": ["copilot", "codex", "gemini", "qwen"]
}
```

---

## Files to Create

### Test Infrastructure
- `tests/day-4-smoke-tests.json` — 10 smoke test cases (200+ lines)
- `.ai/scripts/run-smoke-tests.py` — Test runner (300+ lines)

### Results
- `logs/day-[day]-[report]-results.json` — Test results (generated)
- `logs/day-[day]-[report].md` — Completion report

### Verification
- `logs/workflow.jsonl` — All command executions (appended)
- `logs/tool-performance.jsonl` — Tool metrics (appended)

---

## Smoke Test Structure

```python
# Example smoke test case
{
  "test_id": 1,
  "name": "Normal Mode: Rank 1 Succeeds",
  "input": "/create blog-posts",
  "expected": {
    "status": "success",
    "tool": "copilot",
    "tool_rank": 1,
    "fallback_used": False,
    "logs_generated": True
  },
  "validations": [
    "output is not empty",
    "workflow.jsonl has entry with tool=copilot",
    "tool-performance.jsonl has latency entry"
  ]
}
```

---

## Success Criteria (Day 4)

✅ All 10 smoke tests passing  
✅ Phase 2a + Phase 1 integrated  
✅ Logs generated correctly  
✅ All CLI flags working  
✅ All error paths tested  
✅ End-to-end flow verified  

---

## Time Budget

| Task | Time |
|------|------|
| Setup | 5 min |
| Create test suite | 20 min |
| Create test runner | 30 min |
| Execute tests | 15 min |
| Verify logs | 10 min |
| Integration check | 10 min |
| Completion report | 15 min |
| **Total** | **~105 min** |

---

## Known Considerations

1. **Mock Tool Execution:** Uses mock tools (no actual tool adapters). In production, would call real tools.

2. **Logging Location:** Appends to existing workflow.jsonl and tool-performance.jsonl files. Clear old logs if needed.

3. **Error Testing:** Some tests deliberately create errors. This is expected and validated.

4. **Performance Metrics:** Mock execution has randomized metrics. Production would have real performance data.

---

## Rollback Plan

If smoke tests fail:
1. Check Phase 2a still works: `python3 .ai/scripts/test-flag-parser.py`
2. Check Phase 1 still works: `python3 .ai/scripts/test-tool-router.py`
3. Check integration logic in smoke test runner
4. Verify log files exist and are writable
5. Check tool registry and command routing are loaded correctly

---

## What Comes After Day 4

Once smoke tests pass:
- ✅ Days 5-7: Refinement + optimization
- ✅ Ready for production integration
- ✅ Ready for real tool adapters

---

**Document Status:** Ready for Day 4 execution  
**Last Updated:** 2026-04-13  
**Version:** 1.0  
**Owner:** guide-agent

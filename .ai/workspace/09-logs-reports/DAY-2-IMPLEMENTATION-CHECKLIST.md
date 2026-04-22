# Day 2 Implementation Checklist — Phase 2a CLI Layer

**Date:** 2026-04-13  
**Status:** Ready for Execution  
**Objective:** Integrate flag parsing into guide-agent system prompt

---

## Phase 2a Architecture (Quick Reference)

```
User Input: "/create blog-posts --tool qwen"
    ↓
[NEW: Phase 2a] Tokenize → Extract → Parse & Validate Flags
    ↓
[EXISTING: Phase 1] Route command to tool (respecting flags)
    ↓
[Output] Content + logs
```

**Required Files (All Ready):**
- ✅ `.ai/tool-registry.json` — Tool specs + availability
- ✅ `.ai/GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM-PHASE2A.md` — Flag parsing functions (pseudocode)
- ✅ `.ai/cli-layer/flag-parser.md` — Parsing logic reference
- ✅ `.ai/cli-layer/tool-router.md` — Routing logic reference
- ✅ `.ai/cli-layer/error-handling.md` — Error response templates (just created)

---

## Implementation Steps (Sequential)

### Step 1: Add Flag Parsing to Guide-Agent System Prompt
**Time:** ~30 min

**Input:** 
- `.ai/GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM-PHASE2A.md` (pseudocode)
- `.ai/cli-layer/error-handling.md` (error templates)

**Output:** Updated guide-agent system prompt with Phase 2a code

**Actions:**
- [ ] Read GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM-PHASE2A.md completely
- [ ] Copy tokenize() function into guide-agent system prompt
- [ ] Copy extract_command_and_flags() function
- [ ] Copy parse_and_validate_flags() function
- [ ] Copy execute_user_command() integration wrapper
- [ ] Import error-handling.md error functions
- [ ] Add phase ordering comment: "Phase 2a (CLI) runs BEFORE Phase 1 (Multi-Tool)"
- [ ] Update guide-agent memory to reference Phase 2a status

**Success Criteria:**
- All 3 core functions present in system prompt
- execute_user_command() has Phase 2a → Phase 1 flow
- Error handling integrated before Phase 1 routing

---

### Step 2: Verify Tool Registry Compatibility
**Time:** ~10 min

**Input:** `.ai/tool-registry.json`

**Output:** Confirmation that tool registry matches requirements

**Actions:**
- [ ] Open `.ai/tool-registry.json`
- [ ] Verify `available_tools` array exists
- [ ] Verify `tool_specs` object has all 6 CLI tools (copilot, codex, gemini, qwen, opencode, kilo)
- [ ] Verify each tool has: name, status, specs (context, cost, latency), rank, optimization
- [ ] Confirm status values are: "available" or "unavailable"
- [ ] Confirm unavailable tools have "reason" and "detailed_reason" fields

**Success Criteria:**
- All 6 tools registered
- Status field matches parse_and_validate_flags() expectations
- Rank numbers are accurate (1-6)

---

### Step 3: Create Test Suite
**Time:** ~20 min

**Input:** 
- `.ai/GUIDE-AGENT-SYSTEM-PROMPT-ADDENDUM-PHASE2A.md` (test cases)
- `.ai/cli-layer/error-handling.md` (error test cases)

**Output:** `tests/day-2-flag-parser-tests.json` with 10 test cases

**Actions:**
- [ ] Create `tests/day-2-flag-parser-tests.json` file
- [ ] Copy 5 flag parser test cases from ADDENDUM-PHASE2A.md (Test 1-5)
- [ ] Add 5 error handler test cases from error-handling.md (Tests 6-10)
- [ ] Ensure each test has: input, expected_tokens, expected_command, expected_flags, expected_valid, expected_result
- [ ] Format as JSON array for easy parsing

**Success Criteria:**
- 10 complete test cases in JSON format
- Each test case is independent and runnable
- Test cases cover: normal, forced, explain, parallel, and all 5 error types

---

### Step 4: Create Test Runner Script
**Time:** ~15 min

**Input:** `tests/day-2-flag-parser-tests.json`

**Output:** `.ai/scripts/test-flag-parser.py` (executable test suite)

**Actions:**
- [ ] Create `.ai/scripts/test-flag-parser.py`
- [ ] Write test_tokenize() function (tests tokens)
- [ ] Write test_extract_command_and_flags() function (tests separation)
- [ ] Write test_parse_and_validate_flags() function (tests parsing + validation)
- [ ] Write main() that loads test cases from JSON and runs all tests
- [ ] Add pass/fail counter with summary output
- [ ] Add verbose mode for debugging individual test cases

**Success Criteria:**
- Script runs all 10 tests without errors
- Output shows pass/fail for each test
- Summary shows total passes vs failures
- Can be run with: `python3 .ai/scripts/test-flag-parser.py --verbose`

---

### Step 5: Run Full Test Suite
**Time:** ~10 min

**Input:** 
- Guide-agent system prompt (with Phase 2a code)
- `tests/day-2-flag-parser-tests.json` (test cases)
- `.ai/scripts/test-flag-parser.py` (test runner)

**Output:** `logs/day-[day]-[report]-results.json` (results)

**Actions:**
- [ ] Execute: `python3 .ai/scripts/test-flag-parser.py`
- [ ] Capture output to `logs/day-[day]-[report]-results.json`
- [ ] Verify all 10 tests pass
- [ ] If any fail: debug using verbose mode
- [ ] Fix guide-agent code if needed
- [ ] Re-run until all pass

**Success Criteria:**
- 10/10 tests passing
- All error handlers return correct messages
- All valid commands parse correctly
- Test results logged with timestamp

---

### Step 6: Create Integration Verification Checklist
**Time:** ~5 min

**Input:** CLAUDE.md (startup sequence)

**Output:** `.ai/INTEGRATION-VERIFICATION.md` (go/no-go checklist)

**Actions:**
- [ ] Verify Step 1.6 in CLAUDE.md loads CLI layer files (already done)
- [ ] Verify guide-agent reads tool-registry.json during startup
- [ ] Verify guide-agent calls tokenize() before Phase 1 routing
- [ ] Verify error-handling.md is accessible when needed
- [ ] Verify state.json updated with last_flags after each command
- [ ] Create verification script that checks file existence + readability

**Success Criteria:**
- All 6 files present and readable
- Guide-agent startup sequence valid
- CLAUDE.md references correct versions

---

### Step 7: Create Day 2 Completion Report
**Time:** ~10 min

**Input:**
- Test results from Step 5
- Integration verification from Step 6

**Output:** `logs/day-[day]-[report].md` (summary + status)

**Actions:**
- [ ] Document completion of all 7 steps
- [ ] Include test pass rates
- [ ] List all files created/modified
- [ ] Note any issues encountered + fixes applied
- [ ] Provide handoff to Day 3 (tool-router implementation)
- [ ] Update CLAUDE.md summary with Phase 2a status

**Success Criteria:**
- Clear summary of what was completed
- Test results attached
- Ready for Day 3 work

---

## Files Created/Modified in Day 2

### Created
- ✅ `.ai/cli-layer/error-handling.md` (165 lines)
- [ ] `tests/day-2-flag-parser-tests.json` (in progress)
- [ ] `.ai/scripts/test-flag-parser.py` (in progress)
- [ ] `logs/day-[day]-[report]-results.json` (in progress)
- [ ] `.ai/INTEGRATION-VERIFICATION.md` (in progress)
- [ ] `logs/day-[day]-[report].md` (in progress)

### Modified
- [ ] Guide-agent system prompt (add Phase 2a code)
- [ ] `CLAUDE.md` (update Phase 2a status in summary)
- [ ] `.ai/memory/state.json` (add last_flags, phase_2a_enabled)

---

## Execution Order (Do Not Skip)

1. **Step 1** → Guide-agent integration (foundation)
2. **Step 2** → Tool registry verification (prevents test failures)
3. **Step 3** → Test suite creation (before running tests)
4. **Step 4** → Test runner script (infrastructure)
5. **Step 5** → Run tests (validation)
6. **Step 6** → Integration verification (confidence check)
7. **Step 7** → Completion report (handoff to Day 3)

---

## Success Criteria (Day 2)

✅ All 4 flag parsing functions working (tokenize, extract, parse, validate)  
✅ All 4 execution modes working (normal, explain, forced, parallel)  
✅ All 5 error handlers working (invalid tool, unavailable, conflicts, insufficient)  
✅ 10/10 test cases passing  
✅ Integration verified (Phase 2a → Phase 1 flow correct)  
✅ All files present + properly owned  
✅ State management updated with Phase 2a tracking  

---

## Rollback Plan (If Issues Arise)

If any step fails:

1. **Test failure?** → Debug with verbose mode, fix guide-agent code, re-run tests
2. **Integration issue?** → Check CLAUDE.md Step 1.6 loads files correctly
3. **Tool registry mismatch?** → Verify tool names match between registry + guide-agent
4. **State tracking broken?** → Reset `.ai/memory/state.json` and restart

If rollback needed:
```bash
# Restore v3.2 files (Phase 1 only, no CLI)
cp .ai/archive/commands_v3.2.0.md .ai/commands.md
# This disables Phase 2a but maintains Phase 1 functionality
```

---

## Time Budget

- Step 1: 30 min (flag parsing integration)
- Step 2: 10 min (tool registry check)
- Step 3: 20 min (test suite creation)
- Step 4: 15 min (test runner script)
- Step 5: 10 min (run tests)
- Step 6: 5 min (integration verification)
- Step 7: 10 min (completion report)

**Total: ~100 minutes** (plus debugging if needed)

---

## Next Steps (After Day 2)

Once all steps complete with ✅:
- Day 3: Implement tool-router (routing logic for 4 execution modes)
- Day 4: Run smoke tests (actual commands via CLI flags)
- Days 5-7: Refinement + optimization

**Handoff ready:** All Phase 2a prerequisites met for Day 3 tool-router implementation.

---

**Document Status:** Ready for Day 2 execution  
**Last Updated:** 2026-04-13  
**Version:** 1.0  
**Owner:** guide-agent (read-only reference)

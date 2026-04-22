# CLI Layer — Visual Architecture
**Phase 2a Design Document**

---

## Diagram 1: System Architecture (Phase 1 vs Phase 2)

```
═══════════════════════════════════════════════════════════════════════════════

PHASE 1 (Current)                      PHASE 2 (With CLI Layer)
─────────────────                      ─────────────────────────

User Input                             User Input
   │                                      │
   │ /create blog-posts                  │ /create blog-posts --tool gemini
   │                                      │
   ▼                                      ▼
Guide-Agent                            Guide-Agent
   │                                      │
   │ Parse Command                       │ Parse Command + Flags
   │ → /create blog-posts                │ → /create blog-posts
   │                                      │ → --tool gemini
   ▼                                      ▼
Tool Selector                          CLI Flag Handler (NEW)
   │                                      │
   │ Auto-select Rank 1                 │ --tool flag? → Force tool
   │ (Claude for this)                  │ --explain-routing? → Return explanation only
   │                                      │ --prefer flag? → Set preference hint
   ▼                                      │ --parallel? → Run both tools
Tool Adapter                            │
   │                                      ▼
   │ Load Claude adapter                Tool Selector
   │ State sync                          │
   │                                      │ Auto-select OR forced tool
   ▼                                      │
Execute                                ▼
   │                                      Tool Adapter
   │ Claude generates content            │
   │                                      │ Load selected tool adapter
   ▼                                      │ State sync
Output                                 │ (may run 2 tools in parallel)
   │                                      ▼
   │ post_1_claude_v1.md                Execute
   │                                      │
   ▼                                      │ Single tool OR dual tools
Log + Return                           │ (concurrent execution)
   │                                      │
   │ "Tool: claude"                      ▼
   │ "Status: success"                  Output
                                        │
                                        │ post_1_[tool]_v1.md
                                        │ post_1_[tool2]_v1.md (if parallel)
                                        │
                                        ▼
                                        Log + Return
                                        │
                                        │ "Tool forced: gemini"
                                        │ "Execution mode: parallel"
                                        │ "Status: success_both"

═══════════════════════════════════════════════════════════════════════════════
```

---

## Diagram 2: Flag Parsing Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          USER INPUT PARSING                                  │
└──────────────────────────────────────────────────────────────────────────────┘

Input: /create blog-posts --tool gemini --prefer claude --explain-routing
         │                   │          │                │
         │                   │          │                └─ Flag 3: explain
         │                   │          └────────────────── Flag 2: prefer
         │                   └─────────────────────────────── Flag 1: tool
         └──────────────────────────────────────────────────── Command

         ▼

┌──────────────────────────────────────────────────────────────────────────────┐
│ Parser (NEW in Phase 2)                                                      │
│                                                                              │
│  Step 1: Extract command                                                    │
│  ├─ command = "/create blog-posts"                                          │
│  └─ flags = {--tool, --prefer, --explain-routing}                           │
│                                                                              │
│  Step 2: Validate flags                                                     │
│  ├─ --tool: is "gemini" valid? → YES                                        │
│  ├─ --prefer: is "claude" available? → YES                                  │
│  └─ --explain-routing: boolean flag → YES                                   │
│                                                                              │
│  Step 3: Check for conflicts                                                │
│  ├─ --tool + --explain-routing?                                             │
│  │  └─ ERROR: Can't force AND explain (mutually exclusive)                  │
│  └─ --parallel + --tool?                                                    │
│     └─ WARNING: --tool overrides --parallel (specify both tools manually)    │
└──────────────────────────────────────────────────────────────────────────────┘

         ▼

Parsed Structure:
{
  "command": "/create blog-posts",
  "command_type": "blog-posts",
  "flags": {
    "tool": "gemini",
    "tool_forced": true,
    "prefer": "claude",
    "explain_routing": true,
    "parallel": false
  },
  "context": {
    "brand_voice": [...],
    "keyword_maps": [...]
  }
}

         ▼

Branch by flag priority:

  explain_routing=true? ──YES──> Execute EXPLAIN mode (return explanation)
      │
      NO
      │
      ▼
  tool_forced? ──YES──> Execute FORCED mode (skip fallback chain)
      │
      NO
      │
      ▼
  parallel? ──YES──> Execute PARALLEL mode (run 2 tools concurrently)
      │
      NO
      │
      ▼
  prefer set? ──YES──> Execute PREFER mode (hint for fallback)
      │
      NO
      │
      ▼
  Execute NORMAL mode (auto-select + fallback chain)

```

---

## Diagram 3: Tool Selection Decision Tree (With CLI Flags)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                         TOOL SELECTION LOGIC                                 │
└──────────────────────────────────────────────────────────────────────────────┘

Command: /create blog-posts
Flags: none (normal mode)

                              START
                                │
                    ┌───────────┴────────────┐
                    │                        │
                 Explain          Force Tool
                 Routing?         Selected?
                    │                │
                   NO              NO
                    │                │
                    ▼                ▼
            ┌───────────────┐   Load Rank 1 Tool
            │ Return        │   (Claude for /create)
            │ Explanation   │        │
            │ Only (exit)   │        ▼
            └───────────────┘   Execute with Claude
                                     │
                                    Did it succeed?
                                  /        \
                            YES /            \ NO
                              /                \
                        ┌────────┐        ┌──────────────┐
                        │ Output │        │ Check Prefer │
                        │ saved  │        │ Hint setting │
                        └────────┘        └──────────────┘
                                                  │
                                    ┌─────────────┴─────────────┐
                                    │                           │
                                 Prefer set?               Prefer not set?
                                    │                           │
                                   YES                          NO
                                    │                           │
                                    ▼                           ▼
                          Load preferred tool         Load Rank 2 Tool
                          (skip Rank 2)               (Gemini)
                                    │                           │
                                    └──────────┬────────────────┘
                                               │
                                        Execute Tool
                                               │
                                          Success?
                                         /       \
                                       YES        NO
                                       /           \
                                  Output         Try Rank 3?
                                                    │
                                        ┌───────────┴──────────┐
                                        │                      │
                                      YES                     NO
                                        │                      │
                                        ▼                      ▼
                                  Load Rank 3            ERROR
                                  (Copilot)             Return
                                        │              failure
                                        ▼              response
                                    Execute
                                        │
                                   Success?
                                   /    \
                                YES      NO
                               /          \
                          Output       ERROR


VARIATIONS WITH FLAGS:
══════════════════════════════════════════════════════════════════════════════

--tool gemini:
  Skip normal selection
  Load gemini adapter directly
  If fails → ERROR (no fallback)

--explain-routing:
  Load ranking for command
  Get performance metrics
  Return explanation
  EXIT (no execution)

--prefer gemini:
  Follow normal ranking
  On fallback: jump to preferred tool
  Skip intermediate ranks

--parallel:
  Load Rank 1 + Rank 2
  Execute both simultaneously
  Return both outputs
  No fallback (both run or error)

```

---

## Diagram 4: Execution Modes Timeline

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        EXECUTION MODES COMPARISON                            │
└──────────────────────────────────────────────────────────────────────────────┘

MODE 1: NORMAL (Default, Phase 1)
─────────────────────────────────

Time →
 0s  Start Claude (Rank 1)
 │
 4s  Claude returns ✓
     │
     └──> Output saved
          Log: tool=claude, rank=1
          Return response

Total: 4 seconds


MODE 2: FORCED (New, Phase 2)
────────────────────────────

Time →
 0s  Start Gemini (forced)
 │
 3s  Gemini returns ✓
     │
     └──> Output saved
          Log: tool=gemini, tool_forced=true
          Return response

Total: 3 seconds (if tool was faster)


MODE 3: EXPLAIN (New, Phase 2)
──────────────────────────────

Time →
 0s  Parse command type: /create blog-posts
 │
 0.1s Load ranking from commands-multi-tool.md
 │
 0.2s Get performance metrics from logs
 │
 0.3s Format explanation
      │
      └──> Return explanation only
           (NO execution, NO content created)

Total: 0.3 seconds


MODE 4: FALLBACK (Phase 1, now with PREFER)
─────────────────────────────────────────

Time →
 0s  Start Claude (Rank 1)
 │
 4s  Claude times out ✗
 │
 4.1s Check fallback
      │
      └─ If --prefer gemini: Jump to Gemini
      └─ Else: Jump to Rank 2 (Gemini anyway)
 │
 7s  Gemini returns ✓
     │
     └──> Output saved (gemini version)
          Log: tool=gemini, rank=2, fallback_from=claude
          Return response

Total: 7 seconds (fallback added 3s delay)


MODE 5: PARALLEL (New, Phase 2)
───────────────────────────────

Time →
 0s  Start Claude (Rank 1) + Gemini (Rank 2) simultaneously
 │
 │  Claude: ▬▬▬▬▬▬▬▬▬▬▬▬▬ (4 seconds)
 │  Gemini: ▬▬▬▬▬▬▬▬▬▬ (3 seconds)
 │
 3s  Gemini returns ✓ (wait for both)
 │
 4s  Claude returns ✓
     │
     └──> Both outputs saved
          post_1_claude_v1.md
          post_1_gemini_v1.md
          │
          └──> Return side-by-side comparison
               Log: tool=claude,gemini, execution_mode=parallel
               Return response

Total: 4 seconds (only slightly slower than single tool!)

Benefit: Get both outputs in 4s instead of 8s (if sequential)


═══════════════════════════════════════════════════════════════════════════════
SUMMARY TABLE:

Mode            Time    Tools Executed  Outputs Created  Best For
────────────────────────────────────────────────────────────────────────
Normal          ~4s    1 tool          1 file           Default (quality)
Forced          ~3s    1 tool (forced) 1 file           Testing/override
Explain         ~0.3s  0 tools         0 files          Understanding choice
Fallback        ~7s    2 tools         1 file           Error recovery
Parallel        ~4s    2 tools         2 files          Comparing quality

═══════════════════════════════════════════════════════════════════════════════
```

---

## Diagram 5: State Updates Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        STATE MANAGEMENT UPDATES                              │
└──────────────────────────────────────────────────────────────────────────────┘

USER COMMAND WITH FLAGS:
/create blog-posts --tool gemini

         ▼

┌────────────────────────────────────────────────────────────────┐
│ Guide-Agent Startup (reads current state)                      │
│                                                                │
│ Load: .ai/memory/state.json                                   │
│   {                                                            │
│     "last_command": "...",                                    │
│     "last_tool": "claude",                                    │
│     "tokens_budget": 150000,                                  │
│     "pipeline_stage": "create"                                │
│   }                                                            │
│                                                                │
│ Load: .ai/memory/multi-tool-state/gemini.session.json         │
│   {                                                            │
│     "tokens_used_this_session": 5000,                         │
│     "cost_usd_this_session": 0.40,                            │
│     "execution_history": [...]                                │
│   }                                                            │
└────────────────────────────────────────────────────────────────┘

         ▼ (Execute command)

GEMINI EXECUTES & SUCCEEDS

         ▼

┌────────────────────────────────────────────────────────────────┐
│ State Updates (after execution)                                │
│                                                                │
│ UPDATE: .ai/memory/state.json                                 │
│   {                                                            │
│     "last_command": "/create blog-posts",                    │
│     "last_tool": "gemini",                 ← NEW              │
│     "last_tool_forced": true,              ← NEW              │
│     "last_execution_mode": "normal",       ← NEW              │
│     "tokens_budget": 141580,               ← DECREMENTED      │
│     "pipeline_stage": "create",                               │
│     "last_updated": "2026-04-13T10:35:00"                    │
│   }                                                            │
│                                                                │
│ UPDATE: .ai/memory/multi-tool-state/gemini.session.json       │
│   {                                                            │
│     "tool_id": "gemini",                                       │
│     "tokens_used_this_session": 13420,    ← INCREMENTED       │
│     "cost_usd_this_session": 1.07,        ← INCREMENTED       │
│     "execution_history": [                                    │
│       {                                                        │
│         "command": "/create blog-posts",                     │
│         "was_forced": true,                ← NEW              │
│         "user_preference": null,           ← NEW              │
│         "execution_mode": "normal",        ← NEW              │
│         "duration_ms": 3100,                                  │
│         "status": "success"                                   │
│       }                                                        │
│     ],                                                         │
│     "performance_metrics": {                                  │
│       "success_rate": 0.98,                                   │
│       "avg_latency_ms": 3050                                  │
│     }                                                          │
│   }                                                            │
│                                                                │
│ APPEND: logs/workflow.jsonl (NEW LINE)                        │
│ {                                                              │
│   "timestamp": "2026-04-13T10:35:00+02:00",                 │
│   "command": "/create blog-posts",                           │
│   "agent": "creator-agent",                                  │
│   "tool": "gemini",                                          │
│   "tool_forced_by_user": true,            ← NEW              │
│   "user_preference": null,                ← NEW              │
│   "execution_mode": "normal",             ← NEW              │
│   "tool_rank": 999,    (forced = no rank)                    │
│   "duration_ms": 3100,                                        │
│   "tokens_used": 8420,                                        │
│   "cost_usd": 0.67,                                           │
│   "status": "success",                                        │
│   "output_file": "content/sovereign/blog-posts/[slug]_[tool]_v[version].md"   │
│ }                                                              │
│                                                                │
│ APPEND: logs/tool-performance.jsonl (NEW LINE)                │
│ {                                                              │
│   "timestamp": "2026-04-13T10:35:00+02:00",                 │
│   "tool": "gemini",                                          │
│   "command": "/create blog-posts",                           │
│   "tool_forced": true,                    ← NEW              │
│   "execution_mode": "normal",             ← NEW              │
│   "duration_ms": 3100,                                        │
│   "tokens_used": 8420,                                        │
│   "cost_usd": 0.67,                                           │
│   "quality_scores": {                                         │
│     "brand_voice": 0.91,                                      │
│     "originality": 0.96,                                      │
│     "readability": 0.87                                       │
│   },                                                          │
│   "status": "success"                                         │
│ }                                                              │
└────────────────────────────────────────────────────────────────┘

         ▼

RETURN TO USER:
✅ Content created: /create blog-posts
→ Generated 3 blog posts about sustainable design
→ Saved to: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
→ Tool: Gemini (forced by user, 3.1s, $0.67)
→ Brand voice: 91% | Originality: 96%

💡 Suggested Next Step: /polish content in content/ --tool claude

```

---

## Diagram 6: Error Handling Flows

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           ERROR SCENARIOS                                    │
└──────────────────────────────────────────────────────────────────────────────┘

SCENARIO 1: Invalid Flag
──────────────────────────

User: /create blog-posts --tool qwen

         ▼

Parser validates tool:
  Is "qwen" in available tools? NO

         ▼

RESPONSE:
❌ Tool not available: qwen
Available tools: claude, gemini
Planned (Phase 2): copilot, codex
Planned (Phase 3): qwen, kilo

Use: /create blog-posts --tool claude


SCENARIO 2: Forced Tool Fails
──────────────────────────────

User: /create blog-posts --tool gemini

         ▼

Gemini executes...
After 5s: TIMEOUT (>300s)

         ▼

Guide-Agent detects:
  Was tool forced? YES
  If forced tool fails → NO FALLBACK

         ▼

RESPONSE:
❌ Forced tool failed: gemini
Error: Timeout (>300 seconds)

Since --tool was specified, fallback chain is skipped.
Options:
  • Retry: /create blog-posts --tool gemini
  • Use different tool: /create blog-posts --tool claude
  • Let system decide: /create blog-posts
  • Understand why: /create blog-posts --explain-routing

Log entry: "tool_forced": true, "status": "failed", "error": "timeout"


SCENARIO 3: Conflicting Flags
──────────────────────────────

User: /create blog-posts --tool claude --explain-routing

         ▼

Parser detects conflict:
  --tool (force tool) + --explain-routing (explain only)
  These are mutually exclusive

         ▼

RESPONSE:
❌ Conflicting flags: --tool + --explain-routing
These flags cannot be used together.

--tool: Force execution with specific tool
--explain-routing: Show explanation only (no execution)

Choose one:
  • Force tool: /create blog-posts --tool claude
  • Explain routing: /create blog-posts --explain-routing


SCENARIO 4: Normal Fallback (Rank 1 Fails)
───────────────────────────────────────────

User: /create blog-posts
(no flags, normal mode)

         ▼

Try Rank 1 (Claude):
  After 6s: ORIGINALITY check fails (12% similarity to competitor blog)
  Threshold: ≤15%, Actual: 12% ✗

         ▼

Trigger fallback:
  Try Rank 2 (Gemini)

         ▼

Gemini executes:
  Returns new content
  Quality check passes
  Success! ✓

         ▼

RESPONSE:
✅ Content created (fallback used)
→ Original tool (Claude) rejected due to originality check
→ Automatically retried with Gemini (Rank 2)
→ Saved to: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
→ Tool: Gemini (fallback from Claude, 3.1s, $0.67)
→ Originality: 94% ✓

Log entry: "tool": "gemini", "tool_rank": 2, "fallback_from": "claude"


SCENARIO 5: Prefer Flag with Rank 1 Success
──────────────────────────────────────────────

User: /create blog-posts --prefer gemini

         ▼

Try Rank 1 (Claude):
  Executes successfully
  Quality checks pass
  Returns content ✓

         ▼

Since Rank 1 succeeded:
  Ignore --prefer hint
  Use Claude output

         ▼

RESPONSE:
✅ Content created: /create blog-posts
→ Generated 3 blog posts
→ Saved to: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
→ Tool: Claude (Rank 1, 4.2s, $0.25)
→ (Preference hint ignored because primary tool succeeded)

Log entry: "tool": "claude", "user_preference": "gemini", "used_preference": false


SCENARIO 6: Parallel Mode Partial Success
──────────────────────────────────────────

User: /create blog-posts --parallel

         ▼

Run Claude + Gemini simultaneously

         ▼

After 3s: Gemini returns ✓
After 4.5s: Claude times out ✗

         ▼

Result: Gemini succeeded, Claude failed

         ▼

RESPONSE:
⚠️ Partial success (parallel mode)
→ Claude (Rank 1): TIMEOUT
→ Gemini (Rank 2): SUCCESS ✓

Created:
  content/sovereign/blog-posts/[slug]_[tool]_v[version].md

Not created:
  content/sovereign/blog-posts/[slug]_[tool]_v[version].md (timeout)

Choose one or retry:
  /create blog-posts --tool claude (force retry)
  /create blog-posts --tool gemini (use working version)

Log entries:
  Gemini: "status": "success"
  Claude: "status": "timeout"

```

---

## Diagram 7: Explain Routing Output Format

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                        --explain-routing OUTPUT                              │
└──────────────────────────────────────────────────────────────────────────────┘

USER COMMAND:
/create blog-posts --explain-routing

         ▼

SYSTEM EXECUTES:
  1. Parse: command = /create blog-posts
  2. Load: .ai/commands-multi-tool.md
  3. Find: tool rankings for "blog-posts"
  4. Load: .ai/tool-adapters/ specs
  5. Get: logs/tool-performance.jsonl metrics
  6. Format: human-readable explanation
  7. Return (no command execution)

         ▼

RESPONSE (Text):

┌────────────────────────────────────────────────────────────────────────────┐
│                                                                            │
│  🧭 TOOL SELECTION EXPLANATION                                            │
│  Command: /create blog-posts                                              │
│                                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  RANKING & PERFORMANCE METRICS                                            │
│  ────────────────────────────────────────────────────────────────────    │
│                                                                            │
│  📊 Rank 1: Claude                                                        │
│     ├─ Latency: 4.2s (average over 12 runs)                              │
│     ├─ Cost: $0.25 per command                                            │
│     ├─ Success Rate: 98% (11/12 succeeded)                                │
│     ├─ Quality:                                                           │
│     │  ├─ Brand Voice: 94% (threshold: ≥92%) ✓                           │
│     │  ├─ Originality: 97% (threshold: ≤15% diff) ✓                      │
│     │  └─ Readability: 89% (threshold: ≥65) ✓                            │
│     └─ Why Rank 1? Content quality is critical for blog posts             │
│                                                                            │
│  📊 Rank 2: Gemini (Fallback)                                             │
│     ├─ Latency: 3.1s (average over 8 runs)                               │
│     ├─ Cost: $0.08 per command (cheaper!)                                 │
│     ├─ Success Rate: 96% (7/8 succeeded)                                  │
│     ├─ Quality:                                                           │
│     │  ├─ Brand Voice: 91% (threshold: ≥92%) ✗ (slightly lower)          │
│     │  ├─ Originality: 95% (threshold: ≤15% diff) ✓                      │
│     │  └─ Readability: 88% (threshold: ≥65) ✓                            │
│     └─ Why Rank 2? Fast + cheap, but brand voice slightly lower           │
│                                                                            │
│  📊 Rank 3: Copilot (Phase 2, Not Yet Available)                          │
│     ├─ Status: Planned for Phase 2                                        │
│     ├─ Expected: Fast (2.5s), moderate cost ($0.15)                       │
│     └─ Use Case: Parallel execution or Claude fallback failure            │
│                                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  DECISION LOGIC                                                           │
│  ────────────────────────────────────────────────────────────────────    │
│                                                                            │
│  For /create blog-posts:                                                  │
│  ✅ Brand voice consistency is critical (threshold: 92%)                  │
│     → Claude excels at this (94%)                                         │
│  ✅ Originality is required (≤15% similarity to competitors)              │
│     → Both tools pass this check                                          │
│  ✅ Fallback available if needed (Gemini)                                 │
│     → Cost tradeoff: +$0.17 vs guaranteed quality                         │
│                                                                            │
│  SELECTED: Claude (Rank 1)                                                │
│  FALLBACK: Gemini (Rank 2, if Claude times out or fails quality gate)     │
│                                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  OVERRIDE OPTIONS                                                         │
│  ────────────────────────────────────────────────────────────────────    │
│                                                                            │
│  Force Claude (same as auto):                                             │
│    /create blog-posts --tool claude                                       │
│                                                                            │
│  Force Gemini (cheaper, slightly lower quality):                          │
│    /create blog-posts --tool gemini                                       │
│                                                                            │
│  Get both outputs side-by-side:                                           │
│    /create blog-posts --parallel                                          │
│                                                                            │
│  Prefer Gemini as fallback (if Claude fails):                             │
│    /create blog-posts --prefer gemini                                     │
│                                                                            │
│  ────────────────────────────────────────────────────────────────────    │
│  EXPLANATION COMPLETE                                                     │
│                                                                            │
│  Ready to execute? Remove --explain-routing and run:                      │
│    /create blog-posts                                                     │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagram 8: Complete Request → Response Lifecycle (With CLI)

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     FULL CLI LAYER LIFECYCLE                                 │
└──────────────────────────────────────────────────────────────────────────────┘

TIME    PHASE                    ACTIONS
────────────────────────────────────────────────────────────────────────────────

T=0s    INPUT
        └─ User: /create blog-posts --tool gemini

T=0.01s PARSE & VALIDATE
        ├─ Extract command: /create blog-posts
        ├─ Extract flags: {tool: "gemini"}
        ├─ Validate tool: Is "gemini" available? YES
        ├─ Check conflicts: None
        └─ Status: VALID

T=0.05s LOAD STATE
        ├─ Read: .ai/memory/state.json
        │  └─ Current tokens: 150000
        ├─ Read: .ai/memory/multi-tool-state/gemini.session.json
        │  └─ Gemini tokens used: 5000
        └─ Status: STATE LOADED

T=0.1s  FLAG HANDLING
        ├─ Flag: --tool gemini
        ├─ Action: Force tool selection
        ├─ Skip: Normal ranking + fallback chain
        ├─ Load: .ai/tool-adapters/gemini-adapter.md
        └─ Status: TOOL SELECTED

T=0.2s  CONTEXT INJECTION
        ├─ Load: content/sovereign/reference/brand-voice/style-rules.md (summary)
        ├─ Load: content/sovereign/reference/market-positioning.md (summary)
        ├─ Load: content/sovereign/_references/keyword-maps.md (pointer)
        ├─ Build: System prompt with context
        └─ Status: CONTEXT INJECTED

T=0.3s  EXECUTION START
        ├─ Tool: Gemini
        ├─ Method: JSON API call
        ├─ Timeout: 300s
        ├─ Budget: 50000 tokens (reserved)
        └─ Status: EXECUTING

T=3.1s  EXECUTION COMPLETE
        ├─ Result: Success ✓
        ├─ Output: 3 blog posts (markdown)
        ├─ Quality check:
        │  ├─ Brand voice: 91% (passes 92% threshold)
        │  ├─ Originality: 96% (passes ≤15% similarity)
        │  └─ Readability: 88% (passes ≥65 threshold)
        └─ Status: QUALITY GATES PASSED

T=3.2s  OUTPUT SAVED
        ├─ File: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
        ├─ File: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
        ├─ File: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
        └─ Status: FILES SAVED

T=3.3s  STATE UPDATED
        ├─ Update: .ai/memory/state.json
        │  ├─ last_tool: "gemini"
        │  ├─ last_tool_forced: true ← NEW
        │  └─ tokens_budget: 141580 (decremented)
        ├─ Update: gemini.session.json
        │  ├─ tokens_used: 13420 (incremented)
        │  ├─ cost_usd: 1.07 (incremented)
        │  └─ execution_history: [new entry]
        └─ STATUS: STATE UPDATED

T=3.4s  LOGGING
        ├─ Append: logs/workflow.jsonl
        │  ├─ command: "/create blog-posts"
        │  ├─ tool: "gemini"
        │  ├─ tool_forced_by_user: true ← NEW
        │  ├─ duration_ms: 3100
        │  ├─ status: "success"
        │  └─ output_file: "..."
        ├─ Append: logs/tool-performance.jsonl
        │  ├─ tool: "gemini"
        │  ├─ command: "/create blog-posts"
        │  ├─ duration_ms: 3100
        │  ├─ cost_usd: 0.67
        │  ├─ quality_scores: {...}
        │  └─ status: "success"
        └─ STATUS: LOGGED

T=3.5s  RESPONSE GENERATION
        ├─ Format: Markdown summary
        ├─ Include: Files created, tool used, metrics
        ├─ Include: Quality scores
        ├─ Include: Next step suggestion
        └─ STATUS: READY TO RETURN

T=3.5s  RETURN TO USER
        │
        └─ ✅ Content created: /create blog-posts
           → Generated 3 blog posts about sustainable design
           → Saved to: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
           → Tool: Gemini (forced by user, 3.1s, $0.67)
           → Brand voice: 91% | Originality: 96%
           
           💡 Suggested Next Step: /polish content in content/


TOTAL TIME: 3.5 seconds
(Execution: 3.1s + Overhead: 0.4s)

```

---

## Summary: CLI Layer Architecture

**What gets added in Phase 2:**

1. **Flag Parser** — Extract `--tool`, `--explain-routing`, `--prefer`, `--parallel` from input
2. **Flag Validator** — Check for valid tools, conflicting flags, etc.
3. **Routing Logic** — Branch to EXPLAIN / FORCED / PREFER / PARALLEL / NORMAL mode
4. **State Extensions** — New fields: `tool_forced`, `user_preference`, `execution_mode`
5. **Logging Extensions** — Track forced tools, preferences, execution modes
6. **Error Handling** — Invalid flags, forced tool failure, conflicts
7. **Performance Explanation** — Show ranking + metrics on `--explain-routing`

**No breaking changes to Phase 1:**
- All Phase 1 commands work unchanged (flags optional)
- Fallback chains still work (with new `--prefer` option)
- State files compatible (new fields additive only)
- Phase 1 logs still work (new fields optional in JSON)

**Estimated implementation:**
- Design: Done (this document)
- Code: 3-4 hours
- Testing: 2-3 hours
- Total: 6-7 hours for Phase 2a

---

Ready to implement, or want adjustments to the design?


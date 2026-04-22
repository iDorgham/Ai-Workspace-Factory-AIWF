# Phase 1 Visual Architecture — Diagrams & Flows

---

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER / CLI / API                             │
│                   "/create blog-posts"                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
                    ┌─────────────────┐
                    │  guide-agent    │  ← Router & orchestrator
                    │                 │
                    │ Loads:          │
                    │ • commands-     │
                    │   multi-tool.md │
                    │ • tool adapters │
                    │ • fallback      │
                    │   routing logic │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │   Claude     │  │   Gemini     │  │   Copilot    │
    │   Adapter    │  │   Adapter    │  │   Adapter    │
    │  (Rank 1)    │  │  (Rank 2)    │  │  (Rank 3)    │
    │              │  │              │  │              │
    │ • Input fmt  │  │ • Input fmt  │  │ • Input fmt  │
    │ • State sync │  │ • State sync │  │ • State sync │
    │ • Fallback   │  │ • Fallback   │  │ • Fallback   │
    │   rules      │  │   rules      │  │   rules      │
    └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
           │                 │                 │
           ↓                 ↓                 ↓
      Claude API        Gemini API         Copilot CLI
    (cloud-hosted)    (cloud-hosted)     (local or web)
           │                 │                 │
           └──────────────────┼─────────────────┘
                              ↓
            ┌──────────────────────────────────┐
            │   Multi-Tool State Management     │
            │                                  │
            │ .ai/memory/                      │
            │ ├─ state.json (global)           │
            │ └─ multi-tool-state/             │
            │    ├─ claude.session.json        │
            │    ├─ gemini.session.json        │
            │    └─ [tool].session.json        │
            └──────────────────────────────────┘
                              ↓
            ┌──────────────────────────────────┐
            │    File Output (Versioned)       │
            │                                  │
            │ content/sovereign/blog-posts/              │
            │ ├─ post_1_claude_v1.md           │
            │ ├─ post_1_gemini_v1.md           │
            │ └─ post_1.md (merged)            │
            │                                  │
            │ logs/                            │
            │ ├─ workflow.jsonl (tool-tagged)  │
            │ └─ tool-performance.jsonl        │
            └──────────────────────────────────┘
```

---

## 2. Tool Selection Decision Tree

```
                    Command: /create blog-posts
                              │
                    ┌─────────┴─────────┐
                    │                   │
            Look up in          Parse parameters
         commands-multi-tool.md  (topic, audience)
                    │                   │
                    └─────────┬─────────┘
                              ↓
                   ┌──────────────────┐
                   │ Rankings:        │
                   │ 1. Claude        │
                   │ 2. Gemini        │
                   │ 3. Copilot       │
                   └────────┬─────────┘
                            │
                ┌───────────┴────────────┐
                │                        │
            Try Claude             Load Claude
         (Rank 1)              adapter & state
                │                        │
                └───────────┬────────────┘
                            ↓
                  ┌──────────────────┐
                  │  Execute with    │
                  │  Claude          │
                  │  (conversational)│
                  └────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
       Success?         Timeout?       Low Quality?
      Originality       (>300s)     (Originality<15%)
       ≥ 15%?              │                │
          │                │                │
         YES              YES              YES
          │                │                │
          ↓                ↓                ↓
      ┌───────┐      ┌──────────┐      ┌──────────┐
      │ SAVE  │      │ TRY      │      │ TRY      │
      │ POST_ │      │ GEMINI   │      │ GEMINI   │
      │ CLAUDE│      │(Rank 2)  │      │(Rank 2)  │
      │_V1.MD │      │with new  │      │with new  │
      │       │      │ prompt   │      │ prompt   │
      └───────┘      │ pattern  │      │ pattern  │
                     └────┬─────┘      └────┬─────┘
                          │                 │
                          ↓                 ↓
                    ┌──────────────┐  ┌──────────────┐
                    │ GEMINI       │  │ GEMINI       │
                    │ Success?     │  │ Success?     │
                    └──────┬───────┘  └──────┬───────┘
                           │                 │
                          YES              YES
                           │                 │
                           ↓                 ↓
                    ┌──────────────┐  ┌──────────────┐
                    │ SAVE         │  │ SAVE         │
                    │ POST_        │  │ POST_        │
                    │ GEMINI_V1.MD │  │ GEMINI_V1.MD │
                    └──────────────┘  └──────────────┘
                           │                 │
                           └────────┬────────┘
                                    ↓
                          ┌──────────────────┐
                          │ UPDATE STATE:    │
                          │ .ai/memory/      │
                          │  state.json      │
                          │  .../multi-tool- │
                          │  state/claude.   │
                          │  session.json    │
                          └────────┬─────────┘
                                   ↓
                          ┌──────────────────┐
                          │ LOG COMMAND:     │
                          │ logs/            │
                          │  workflow.jsonl  │
                          │  tool-perf.jsonl │
                          └────────┬─────────┘
                                   ↓
                          ┌──────────────────┐
                          │ RETURN OUTPUT:   │
                          │ ✓ Success        │
                          │ → Saved to: ...  │
                          │ → Tool: claude   │
                          │ → Cost: $0.25    │
                          └──────────────────┘
```

---

## 3. Tool Rankings by Command Type (Matrix View)

```
┌──────────────────────────────────────────────────────────────────────┐
│           TOOL RANKINGS BY COMMAND TYPE                              │
├──────────────────────┬────────────┬────────────┬────────────┤────────┤
│ COMMAND              │ Rank 1     │ Rank 2     │ Rank 3     │ Reason │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /brand               │ Claude     │ Gemini     │ Copilot    │ Interactive│
│                      │            │            │            │ brand Q&A  │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /research competitors│ Claude     │ Gemini     │ Codex      │ Strategic  │
│                      │            │            │            │ reasoning  │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /scrape all /*       │ Codex      │ OpenCode   │ Claude     │ Code       │
│ /sync                │            │            │            │ specialist │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /create blog-posts   │ Claude ✓✓✓ │ Gemini ✓✓  │ Copilot ✓  │ Brand      │
│ /create landing-pg   │ (94-96%)   │ (92-94%)   │ (90-92%)   │ voice      │
│ /create project-pg   │            │            │            │ quality    │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /polish content      │ Claude     │ Gemini     │ Copilot    │ Cost-      │
│ (≤30 items)          │ (best)     │ (if >30)   │ (fallback) │ aware      │
│ (>30 items)          │ Gemini     │ Claude     │ Copilot    │ selection  │
│                      │ (cheaper)  │ (if fails) │ (fallback) │           │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /optimize images     │ Gemini ✓✓✓ │ Claude ✓✓  │ Codex ✓    │ Multi-     │
│                      │ (multimodal)│(text-only)│ (metadata) │ modal      │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /compare sovereign    │ Claude ✓✓✓ │ Gemini ✓✓  │ Copilot ✓  │ Strategic  │
│ vs competitor        │            │ (large    │            │ diff +     │
│                      │            │  context) │            │ reasoning  │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /review (quality     │ Claude     │ Gemini     │ (manual)   │ Claude:    │
│  gates)              │ (tone)     │ (SEO, ║    │            │ tone       │
│                      │ + Gemini   │  parallel) │            │ Gemini:    │
│                      │ (SEO, ║)   │            │            │ SEO speed  │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /extract brand       │ Claude     │ Gemini     │ Copilot    │ Voice      │
│ /refine voice        │            │            │            │ analysis   │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /archive             │ Claude     │ (Gemini    │ (N/A)      │ Simple     │
│ /export              │            │  future)   │            │ workflow   │
│ /approve             │            │            │            │ task       │
├──────────────────────┼────────────┼────────────┼────────────┼────────┤
│ /memory save|load    │ Claude     │ (N/A)      │ (N/A)      │ State      │
│ /budget check        │            │            │            │ management │
└──────────────────────┴────────────┴────────────┴────────────┴────────┘

Legend:
  ✓✓✓ = Excellent fit (use first)
  ✓✓  = Good fit (fallback tier 1)
  ✓   = Acceptable fit (fallback tier 2)
  ║   = Can run in parallel for speed
```

---

## 4. State Synchronization Flow

```
                    Command Execution
                          │
          ┌───────────────┴───────────────┐
          │                               │
    ┌─────▼──────────┐            ┌──────▼──────────┐
    │ BEFORE Exec    │            │ AFTER Exec      │
    ├────────────────┤            ├─────────────────┤
    │ Read:          │            │ Update:         │
    │                │            │                 │
    │ .ai/memory/    │            │ .ai/memory/     │
    │  state.json    │            │  state.json     │
    │  (global)      │            │  (global)       │
    │                │            │                 │
    │ .ai/memory/    │            │ .ai/memory/     │
    │  multi-tool-   │            │  multi-tool-    │
    │  state/        │            │  state/         │
    │  [tool].json   │            │  [tool].json    │
    │  (tool-        │            │  (tool-         │
    │  specific)     │            │  specific)      │
    │                │            │                 │
    │ Load context:  │            │ Increment:      │
    │ • brand-voice  │            │ • tokens_used   │
    │ • keywords     │            │ • cost_usd      │
    │ • positioning  │            │ • total_commands│
    │                │            │ • successful    │
    └────────────────┘            └─────────────────┘
          │                               │
          │          Execute Tool         │
          └──────────────┬────────────────┘
                         │
                         ↓
           ┌─────────────────────────┐
           │  Claude / Gemini / etc  │
           │  (with loaded context)  │
           │                         │
           │  Process:               │
           │  • Apply brand voice    │
           │  • Check originality    │
           │  • Generate content     │
           │  • Track tokens/cost    │
           └────────────┬────────────┘
                        │
                        ↓
           ┌─────────────────────────┐
           │  Result + Metadata      │
           │                         │
           │ {                       │
           │  "status": "success",   │
           │  "tokens_used": 8420,   │
           │  "cost_usd": 0.25,      │
           │  "duration_ms": 4200,   │
           │  "quality_scores": {    │
           │    "brand_voice": 0.94, │
           │    "originality": 0.97  │
           │  }                      │
           │ }                       │
           └────────────┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ↓               ↓               ↓
   ┌─────────────┐ ┌───────────┐ ┌─────────────┐
   │ Save file   │ │Update     │ │ Log to      │
   │             │ │ state     │ │ JSONL logs  │
   │ content/    │ │           │ │             │
   │ blog-posts/ │ │ .ai/      │ │ logs/       │
   │ post_1_     │ │ memory/   │ │ workflow.   │
   │ [tool]_v1   │ │ state.json│ │ jsonl       │
   │ .md         │ │           │ │ (append)    │
   │             │ │ .ai/      │ │             │
   │             │ │ memory/   │ │ logs/       │
   │             │ │ multi-    │ │ tool-perf.  │
   │             │ │ tool-     │ │ jsonl       │
   │             │ │ state/    │ │ (append)    │
   │             │ │ [tool].   │ │             │
   │             │ │ json      │ │             │
   └─────────────┘ └───────────┘ └─────────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ↓
            ┌──────────────────────────┐
            │ Return to User:          │
            │                          │
            │ ✅ Content created       │
            │ → Saved to: [path]       │
            │ → Tool: [tool_name]      │
            │ → Cost: $0.25            │
            │ → Duration: 4.2s         │
            │                          │
            │ 💡 Next Step: ...        │
            └──────────────────────────┘
```

---

## 5. File Output & Versioning Strategy

```
Multiple Tools, One Command
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scenario A: Claude Succeeds
────────────────────────────
  /create blog-posts
       ↓
  Claude (Rank 1) → Success
       ↓
  content/sovereign/blog-posts/
  └─ post_1_claude_v1.md ← SAVED


Scenario B: Claude Fails, Gemini Succeeds (Fallback)
─────────────────────────────────────────────────────
  /create blog-posts
       ↓
  Claude (Rank 1) → Timeout
       ↓
  Gemini (Rank 2) → Success
       ↓
  content/sovereign/blog-posts/
  └─ post_1_gemini_v1.md ← SAVED
     (Claude attempt abandoned)


Scenario C: Both Claude & Gemini Succeed (Parallel)
───────────────────────────────────────────────────
  /create blog-posts
       ↓
  Claude (Rank 1) ──→ Success
  Gemini (Rank 2) ──→ Success (parallel)
       ↓
  content/sovereign/blog-posts/
  ├─ post_1_claude_v1.md ← Both saved
  └─ post_1_gemini_v1.md

  User chooses:
  /merge --prefer claude
       ↓
  content/sovereign/blog-posts/
  ├─ post_1.md ← ACTIVE (Claude's version)
  └─ post_1_gemini_v1.md → archived


Scenario D: Re-running Same Command
───────────────────────────────────
  /create blog-posts (first time)
  └─ post_1_claude_v1.md (v=1)

  /create blog-posts (second time)
  └─ post_1_claude_v2.md (v=2, incremented)

  Both versions kept for history/comparison
```

---

## 6. Performance Comparison Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL PERFORMANCE PROFILE                     │
├─────────────┬──────────┬──────────┬──────────┬──────────────────┤
│ Metric      │ Claude   │ Gemini   │ Codex    │ When to Use      │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Latency     │          │          │          │                  │
│ (p50)       │ 800ms ✓✓ │ 1200ms   │ 1500ms   │ Claude fastest   │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Latency     │          │          │          │                  │
│ (p95)       │ 3000ms   │ 4500ms   │ 5000ms   │ Claude most      │
│             │ ✓✓       │          │          │ consistent       │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Cost/1M     │ $3-15    │ $0.075   │ $0.5-2   │ Gemini 20-40x    │
│ tokens      │ $$$$     │ $  ✓✓✓   │ $$       │ cheaper than     │
│             │          │          │          │ Claude           │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Context     │ 200k     │ 1M       │ 400k     │ Gemini best for  │
│ window      │          │ ✓✓✓      │          │ large docs       │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Brand       │ 94-96%   │ 92-94%   │ 85%      │ Claude best for  │
│ voice       │ ✓✓✓      │ ✓✓       │ ✓        │ consistent tone  │
│ compliance  │          │          │          │                  │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Multimodal  │ Images   │ Full     │ No       │ Gemini only for  │
│ support     │ only     │ (best) ✓✓│         │ images/video     │
│             │ ✓        │ ✓✓✓      │          │                  │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Success     │ 99.5%    │ 98.8%    │ 98%      │ Claude most      │
│ rate        │ ✓✓✓      │ ✓✓       │ ✓        │ reliable         │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Best for    │ Content, │ Images,  │ Scraping │ All tools        │
│             │ reasoning│ bulk     │ code gen │ specialize       │
│             │          │ work     │          │                  │
├─────────────┼──────────┼──────────┼──────────┼──────────────────┤
│ Rank for    │ 1        │ 2        │ 1 (code) │ Fallback chain:  │
│ content     │ (default)│ (cheap)  │          │ Claude → Gemini  │
│ creation    │          │          │          │                  │
└─────────────┴──────────┴──────────┴──────────┴──────────────────┘

Recommendation by Use Case:
  • Quality-critical → Claude (pay for consistency)
  • Bulk processing → Gemini (save 80% cost)
  • Speed critical → Claude (lowest latency)
  • Large docs → Gemini (1M context)
  • Images/video → Gemini (only multimodal option)
```

---

## 7. Fallback Chain Cascade

```
                    FALLBACK CHAIN: /create blog-posts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                          Start
                            │
                            ↓
                    ┌──────────────────┐
                    │ Attempt Claude   │
                    │ (Rank 1)         │
                    │ • Load context   │
                    │ • Execute        │
                    │ • Validate       │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
        Success           Timeout         Quality
        ✓ Originality    (>300s)          Fails
        ≥ 15%              │           (Orig <15%)
            │                │                │
            │                │                │
        ┌───┴─────┐      ┌───┴─────┐      ┌──┴──────┐
        │ SAVE to │      │ SWITCH  │      │ SWITCH  │
        │ post_1_ │      │ TO      │      │ TO      │
        │ claude_ │      │ GEMINI  │      │ GEMINI  │
        │ v1.md   │      │ (Rank2) │      │ (Rank2) │
        │         │      │ Retry   │      │ Retry   │
        │ DONE ✓  │      │ with    │      │ with    │
        └─────────┘      │ new     │      │ new     │
                         │ prompt  │      │ pattern │
                         └────┬────┘      └────┬────┘
                              │                │
                         ┌────▼────────────┐   │
                         │ Attempt Gemini  │←──┘
                         │ (Rank 2)        │
                         │ • Load context  │
                         │ • Execute       │
                         │ • Validate      │
                         └────────┬────────┘
                                  │
                    ┌─────────────┼──────────────┐
                    │             │              │
                Success        Timeout        Quality
                ✓              (>300s)        Fails
                    │             │              │
                    │             │              │
                ┌───┴──────┐  ┌──┴──────┐  ┌───┴──────┐
                │ SAVE to  │  │ SWITCH  │  │ SWITCH   │
                │ post_1_  │  │ TO      │  │ TO       │
                │ gemini_  │  │ COPILOT │  │ COPILOT  │
                │ v1.md    │  │ (Rank3) │  │ (Rank3)  │
                │          │  │         │  │          │
                │ DONE ✓   │  └────┬────┘  └────┬─────┘
                └──────────┘       │             │
                                   └──────┬──────┘
                                          │
                                    ┌─────▼──────────┐
                                    │ Attempt Copilot│
                                    │ (Rank 3)       │
                                    │ • Execute      │
                                    │ • Validate     │
                                    └────────┬───────┘
                                             │
                                    ┌────────┴────────┐
                                    │                 │
                                  Success          Failure
                                    │                 │
                                    ↓                 ↓
                            ┌──────────────┐  ┌──────────────┐
                            │ SAVE to      │  │ ERROR:       │
                            │ post_1_      │  │ All tools    │
                            │ copilot_v1.md│  │ exhausted    │
                            │              │  │              │
                            │ DONE ✓       │  │ Request      │
                            └──────────────┘  │ manual       │
                                              │ intervention │
                                              └──────────────┘

TOTAL ATTEMPTS: 3 (Claude → Gemini → Copilot)
FAST PATH: ~4s (Claude succeeds on first try) ✓
SLOW PATH: ~30s (all three tools fail)
FALLBACK OVERHEAD: ~1-2s per tool switch
```

---

## 8. Command Flow: Before & After

```
BEFORE (v3.2 - Monolithic)
═══════════════════════════════════════════════════════════

  User: /create blog-posts
      ↓
  guide-agent parses command
      ↓
  Routes to Claude (only option)
      ↓
  Claude executes
      ↓
  ├─ Success? → Save & done ✓
  └─ Fail? → Error. Stop. No alternative. ✗


AFTER (Phase 1 - Multi-Tool)
═════════════════════════════════════════════════════════════

  User: /create blog-posts
      ↓
  guide-agent parses command
      ↓
  Looks up tool rankings: Claude, Gemini, Copilot
      ↓
  Loads Claude adapter & state
      ↓
  Claude executes
      ↓
  ├─ Success & originality ≥ 15%?
  │  └─ → SAVE post_1_claude_v1.md ✓ DONE
  │
  ├─ Timeout or originality < 15%?
  │  └─ Load Gemini adapter & state
  │     └─ Gemini executes
  │        ├─ Success?
  │        │  └─ → SAVE post_1_gemini_v1.md ✓ DONE
  │        └─ Fail?
  │           └─ Load Copilot adapter
  │              └─ Copilot executes
  │                 ├─ Success?
  │                 │  └─ → SAVE post_1_copilot_v1.md ✓ DONE
  │                 └─ Fail?
  │                    └─ → ERROR: All tools failed ✗
  │
  └─ Both Claude & Gemini succeeded (parallel)?
     └─ → SAVE BOTH:
        ├─ post_1_claude_v1.md
        ├─ post_1_gemini_v1.md
        └─ User chooses: /merge --prefer [tool]

Key Improvements:
  ✓ Multiple tools tried before giving up
  ✓ Output choices if multiple succeed
  ✓ Cost optimization (Gemini for bulk)
  ✓ Reliability (fallback chain)
  ✓ Quality A/B testing (compare outputs)
```

---

## 9. State Architecture Overview

```
GLOBAL STATE (One, shared by all tools)
┌────────────────────────────────────────────┐
│ .ai/memory/state.json                      │
├────────────────────────────────────────────┤
│ {                                          │
│   "session": {...},                        │
│   "pipeline_state": {                      │
│     "current_stage": "content_creation",   │
│     "last_command": "/create blog-posts",  │
│     "last_tool": "claude" ← NEW (Phase 1)  │
│     "last_agent": "creator-agent"          │
│   },                                       │
│   "active_content": {                      │
│     "last_created": "post_1_claude_v1.md", │
│     "pending_review": [...]                │
│   }                                        │
│ }                                          │
└────────────────────────────────────────────┘

TOOL-SPECIFIC STATE (One per tool)
┌────────────────────────────────────────────┐
│ .ai/memory/multi-tool-state/               │
│                                            │
│ claude.session.json:                       │
│ ├─ tool_id: "claude"                       │
│ ├─ tokens_used_this_session: 18420         │
│ ├─ context_window_capacity: 200000         │
│ ├─ execution_history:                      │
│ │  ├─ total_commands: 5                    │
│ │  ├─ successful: 5                        │
│ │  ├─ failed: 0                            │
│ │  └─ timed_out: 0                         │
│ └─ performance_metrics:                    │
│    ├─ avg_latency_ms: 3800                 │
│    ├─ success_rate_percent: 100            │
│    └─ cost_usd_this_session: 1.42          │
│                                            │
│ gemini.session.json:                       │
│ ├─ tool_id: "gemini"                       │
│ ├─ tokens_used_this_session: 4200          │
│ ├─ context_window_capacity: 1000000        │
│ ├─ execution_history:                      │
│ │  ├─ total_commands: 2                    │
│ │  ├─ successful: 2                        │
│ │  ├─ failed: 0                            │
│ │  └─ timed_out: 0                         │
│ └─ performance_metrics:                    │
│    ├─ avg_latency_ms: 2100                 │
│    ├─ success_rate_percent: 100            │
│    └─ cost_usd_this_session: 0.16          │
│                                            │
│ [other tools...]                           │
└────────────────────────────────────────────┘

WORKFLOW LOG (Permanent record, tool-tagged)
┌────────────────────────────────────────────┐
│ logs/workflow.jsonl                        │
├────────────────────────────────────────────┤
│ {"timestamp": "2026-04-13T10:22:00+02:00", │
│  "command": "/create blog-posts",          │
│  "agent": "creator-agent",                 │
│  "tool": "claude", ← NEW (Phase 1)         │
│  "tool_rank": 1,                           │
│  "status": "success",                      │
│  "duration_ms": 4200,                      │
│  "tokens_used": 8420,                      │
│  "cost_usd": 0.25}                         │
│                                            │
│ {"timestamp": "2026-04-13T10:30:00+02:00", │
│  "command": "/optimize images",            │
│  "agent": "seo-agent",                     │
│  "tool": "gemini", ← NEW (Phase 1)         │
│  "tool_rank": 1,                           │
│  "status": "success",                      │
│  "duration_ms": 2100,                      │
│  "cost_usd": 0.08}                         │
└────────────────────────────────────────────┘

PERFORMANCE LOG (Tool metrics for ranking)
┌────────────────────────────────────────────┐
│ logs/tool-performance.jsonl ← NEW (Phase 1)│
├────────────────────────────────────────────┤
│ {"timestamp": "2026-04-13T10:22:00+02:00", │
│  "tool": "claude",                         │
│  "command": "/create blog-posts",          │
│  "duration_ms": 4200,                      │
│  "cost_usd": 0.25,                         │
│  "quality_scores": {                       │
│    "brand_voice": 0.94,                    │
│    "originality": 0.97,                    │
│    "readability": 0.89                     │
│  },                                        │
│  "status": "success"}                      │
└────────────────────────────────────────────┘
```

---

This visualization file maps to the actual system. All diagrams are ASCII for durability (no images to break).


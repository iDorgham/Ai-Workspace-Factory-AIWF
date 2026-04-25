# Fallback Routing Logic — Multi-Tool Orchestration
**Owner:** guide-agent  
**Updated:** 2026-04-13

---

## Tool Ranking by Command Type

Every Sovereign command has a ranked list of preferred tools. guide-agent uses this to decide **which tool executes the command**.

### `/brand` — Brand Discovery & Voice Definition
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Excels at interactive, nuanced brand definition | Timeout |
| 2 | Gemini | Good reasoning; large context for survey input | API overload |
| 3 | Copilot | CLI-friendly; fast | Agent unavailable |

**Decision Logic:**
- Default: Claude (interactive best for brand questions)
- If `context > 150k tokens`: Switch to Gemini (1M capacity)
- If Claude times out: Fallback to Gemini
- If both fail: Fallback to Copilot CLI

---

### `/research competitors` — Competitor Discovery
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Web search reasoning + profile synthesis | Timeout |
| 2 | Gemini | Fast; good for candidate scoring | API overload |
| 3 | Gemini CLI | CLI-native; scalable for batch | Web search fails |

**Decision Logic:**
- Default: Claude (best reasoning for nuanced profiles)
- If > 20 competitors to profile: Switch to Gemini (cheaper, faster)
- If parsing fails: Retry with Gemini's different parsing approach
- If both fail: Manual fallback (skip web search, accept user input)

---

### `/scrape *` — Ethical Web Scraping
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Codex CLI | Specialized for scraping logic | Timeout |
| 2 | OpenCode CLI | Code-first; handles complex HTML | API error |
| 3 | Claude | Fallback reasoning for novel scraping patterns | All others fail |

**Decision Logic:**
- Default: Codex (best for scraping-specific code patterns)
- If scraper encounters novel HTML structure: Switch to OpenCode (handles edge cases)
- If both fail: Switch to Claude (pure reasoning; no code execution)
- **CRITICAL:** All scrapers must respect `robots.txt` + enforce 2s rate limits

---

### `/create blog-posts about [topic]` — Content Generation
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Best brand voice compliance (94-96%) | Timeout |
| 2 | Gemini | Cheaper; good compliance (92-94%); larger context | Originality fails |
| 3 | Copilot | Fast fallback; CLI-native | Both fail |

**Decision Logic:**
- Default: Claude (highest brand voice compliance)
- If originality score < 15% after 2 retries: Switch to Gemini (different pattern generation)
- If Gemini also fails: Try Copilot (fresh approach)
- **Quality Gate:** Do NOT export content that fails originality check (locked until revised)

---

### `/create landing pages for [campaign]` — Campaign-Specific Content
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Excellent conversion copy; subtle persuasion | Timeout |
| 2 | Gemini | Good copy; faster for large context | Tone drift |
| 3 | Copilot | Fast fallback | Both fail |

**Decision Logic:**
- Default: Claude (copy quality is critical for conversions)
- If tone compliance < 92%: Switch to Gemini (re-attempt with different voice matrix)
- Both fail: Manual review required before export

---

### `/polish content in content/` — SEO Optimization
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Best SEO knowledge; keyword placement finesse | Timeout |
| 2 | Gemini | Large context; good for bulk optimization | Rate limit |
| 3 | Copilot CLI | Fast; good for keyword density checks | Both fail |

**Decision Logic:**
- Default: Claude (best SEO judgment)
- If > 30 articles to polish: Switch to Gemini (cheaper, parallel-ready)
- If keyword cannibalization detected: Always use Claude (requires reasoning)

---

### `/optimize images in content/` — Image SEO
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Gemini | Multimodal; can analyze actual images | Image count < 5 |
| 2 | Claude | Fallback alt-text generation (no image analysis) | Timeout |
| 3 | Codex CLI | Fast batch image metadata generation | Both fail |

**Decision Logic:**
- Default: Gemini (can see images; better alt-text)
- If images < 5: Can use Claude (not worth Gemini API call)
- If Gemini image processing fails: Fallback to Claude (text-only alt-text)

---

### `/review` — Quality Gate Execution
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Best judgement on tone compliance + edge cases | Timeout |
| 2 | Gemini | Good for bulk SEO review; cheaper | Tone gate fails |
| 3 | (Manual) | Human review (cannot fully automate) | Both fail |

**Decision Logic:**
- Default: Claude (runs all 5 gates, decides if "pass" or "needs revision")
- SEO Gate: Can parallelize with Gemini (cheaper)
- Tone Gate: Always use Claude (most nuanced)
- If > 50% of gates fail: Escalate to human review

---

### `/compare sovereign vs competitor [name]` — Competitive Analysis
| Rank | Tool | Reason | Fallback On |
|------|------|--------|------------|
| 1 | Claude | Strategic diff; identifies positioning gaps | Timeout |
| 2 | Gemini | Large context; good for cross-document analysis | Context too large |
| 3 | Copilot | Fast fallback comparison | Both fail |

**Decision Logic:**
- Default: Claude (best strategic thinking)
- If competitor corpus > 200k tokens: Switch to Gemini (1M context)
- If positioning gap analysis fails: Manual review required

---

## Fallback Decision Tree

```
User issues command "/create blog-posts about [topic]"
    ↓
guide-agent parses → ranks tools → starts with #1
    ↓
├─ Try Claude (rank 1)
│  ├─ Success? → Done. Output to content/sovereign/blog-posts/[slug]_claude.md
│  ├─ Timeout? → Go to Fallback A
│  └─ Originality <15%? → Go to Fallback B
│
├─ Fallback A: Timeout (try Gemini)
│  ├─ Gemini success? → Output to [slug]_gemini.md. Note: "Claude timed out; Gemini completed."
│  └─ Gemini fails? → Go to Fallback C
│
├─ Fallback B: Originality fails (try Gemini with different prompt)
│  ├─ Gemini success + originality ≥ 15%? → Output to [slug]_gemini.md
│  └─ Gemini fails? → Flag for manual revision. Do NOT export.
│
└─ Fallback C: All tools fail
   ├─ Log error to .ai/logs/workflow.jsonl
   ├─ Output: "All tools exhausted. Manual intervention required."
   └─ Halt pipeline (cannot proceed to /review without content)
```

---

## Tool State Across Fallback Chain

When guide-agent switches tools, it must **preserve and pass state**:

### State Handoff Protocol
```
Claude context exhaustion:
1. Claude outputs partial results + "context exhausted" flag
2. guide-agent loads both `.ai/memory/state.json` + `claude.session.json`
3. guide-agent constructs new request for Gemini
4. Gemini receives:
   - Full state context (what Claude had done)
   - Claude's partial output (so Gemini can continue, not restart)
   - Same input parameters
5. Gemini continues from Claude's stopping point
6. Result versioned: [slug]_gemini_v1.md (different from Claude's output)
```

### Conflict Resolution on Fallback
- **Same slug, different tool outputs:**
  - Claude output: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
  - Gemini output: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
  - guide-agent does NOT merge automatically
  - User must choose: `/merge blog-posts --prefer claude` or `--prefer gemini`
  
- **Quality gate comparison:**
  - Both outputs run through `/review`
  - Output with higher quality score becomes primary
  - Lower score marked as "alt_output" in frontmatter

---

## Cost Optimization Strategy

### When to Switch for Cost Reasons
| Command | Tool Order | Savings |
|---------|-----------|---------|
| `/polish content` (>20 articles) | Claude → Gemini | ~80% cheaper |
| `/optimize images` (multimodal) | Gemini → Claude | Gemini ~2x cost but worth it for images |
| `/create blog-posts` (text-only) | Claude (stay) | None; Claude's quality worth the cost |

**Guide-agent heuristic:**
- If processing > 20 items: Offer switch to cheaper alternative
- If user confirms: Proceed with Gemini (cost-optimized)
- If user declines: Stay with Claude (quality-optimized)

---

## Monitoring & Adaptive Routing

### Performance Tracking per Tool
`.ai/logs/tool-performance.jsonl` (new file, append-only):
```json
{
  "timestamp": "2026-04-13T10:22:00+02:00",
  "command": "/create blog-posts",
  "tool": "claude",
  "status": "success",
  "latency_ms": 4200,
  "tokens_used": 8420,
  "cost_usd": 0.25,
  "quality_scores": {
    "brand_voice": 0.95,
    "originality": 0.97,
    "readability": 0.89
  }
}
```

### Adaptive Ranking Update (Monthly)
1. guide-agent aggregates tool performance metrics
2. If Tool B consistently outperforms Tool A on metric X, swap ranks
3. Example: If Gemini's originality score > Claude's for 10 consecutive runs, rank Gemini #1 for that command type
4. Update `.ai/tool-adapters/` adapter files with new rankings

---

## CLI Integration: Tool Selection

When running via CLI (e.g., `sovereign-gemini /create blog-posts`):

**Explicit tool selection:**
```bash
# Force Gemini
sovereign-gemini /create blog-posts --topic sustainable-design

# Force Claude
sovereign-claude /create blog-posts --topic sustainable-design

# Auto-select (guide-agent chooses)
sovereign /create blog-posts --topic sustainable-design
```

**Auto-selection logic:**
- If no tool specified: guide-agent applies ranking rules above
- If tool specified: Use that tool (no fallback unless explicitly allowed)
- Fallback allowed if: `--allow-fallback` flag is passed

---

## Debugging Fallback Decisions

**To understand why a tool was chosen:**
```bash
sovereign /create blog-posts --debug --explain-routing
```

Output:
```
Route decision for "/create blog-posts":
1. Rank 1 (Claude): Available ✅ → Selected
2. (Gemini, Copilot held as fallback)

If Claude fails:
 - Timeout (>300s) → Fallback to Gemini
 - Originality <15% → Fallback to Gemini (retry with different prompt)
 - API error → Fallback to Copilot CLI

Execute command with Claude...
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-04-13 | Initial fallback routing spec for Phase 1 (Claude + Gemini) |


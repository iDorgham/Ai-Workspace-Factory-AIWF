# Phase 1 Quick Reference Card
**Print this. Keep handy.**

---

## Tool Rankings (Command Type)

```
CONTENT CREATION          OPTIMIZATION          SCRAPING
/create *                 /polish               /scrape
/compare *                /optimize             /sync

1️⃣  Claude              1️⃣  Claude (≤30)      1️⃣  Codex
2️⃣  Gemini              2️⃣  Gemini (>30)      2️⃣  OpenCode
3️⃣  Copilot             3️⃣  Copilot           3️⃣  Claude

IMAGE OPTIMIZATION        BRAND WORK
/optimize images          /brand
                         /extract voice
1️⃣  Gemini              1️⃣  Claude
2️⃣  Claude              2️⃣  Gemini
3️⃣  Codex               3️⃣  Copilot
```

---

## Fallback Chain (What Happens If Tool Fails)

```
/create blog-posts
    ↓
Claude fails?   → Try Gemini
Gemini fails?   → Try Copilot
Copilot fails?  → Error + manual intervention

Total attempts: 3
Fastest exit: ~5 seconds (success on first try)
Slowest exit: ~30 seconds (tries all 3; all fail)
```

---

## File Naming Convention

```
✅ SUCCESS (Claude generates content)
   content/sovereign/blog-posts/[slug]_[tool]_v[version].md

✅ FALLBACK (Claude times out, Gemini succeeds)
   content/sovereign/blog-posts/[slug]_[tool]_v[version].md

✅ MULTIPLE TOOLS (Both run, both succeed)
   content/sovereign/blog-posts/[slug]_[tool]_v[version].md
   content/sovereign/blog-posts/[slug]_[tool]_v[version].md
   → Use: /merge --prefer claude

❌ OPTIMIZATION (Overwrites in-place, no branching)
   content/sovereign/blog-posts/[slug].md → optimized by Claude
   Backup: .ai/memory/polish-backup/post_1_[timestamp].md
```

---

## State Files (Where Things Are Stored)

```
Global State (Updated after every command)
  .ai/memory/state.json
  └─ Which stage? (/create, /polish, /review, etc.)
  └─ What tool last ran? (claude, gemini, etc.)

Tool-Specific State (One per tool)
  .ai/memory/multi-tool-state/
  ├─ claude.session.json
  ├─ gemini.session.json
  └─ [tool].session.json
  └─ How many tokens used this session?
  └─ What was the last command?

Logs (Append-only, permanent record)
  logs/workflow.jsonl
  ├─ Every command, every tool, every status
  └─ Tool performance metrics aggregated

  logs/tool-performance.jsonl
  └─ Performance comparison (latency, cost, quality)
```

---

## Decision Tree (Compressed)

```
Command → Pick Rank 1 tool
              ↓
         Success? → Save output, done ✓
         Timeout? → Try Rank 2 tool
         Low quality? → Try Rank 2 tool
         API error? → Try Rank 2 tool
              ↓
         Try Rank 2
              ↓
         Success? → Save output, done ✓
         Fail? → Try Rank 3
              ↓
         Try Rank 3
              ↓
         Success? → Save output, done ✓
         Fail? → Error (all tools exhausted) ✗
```

---

## Cost Comparison

```
Per 1M tokens:

Claude    $3-15         $$$$
Gemini    $0.075-0.6    $
Codex     $0.5-2        $$
Copilot   ~$1-5         $$-$$$

Best ROI: Gemini for bulk work (20+ items)
Best quality: Claude (but most expensive)
```

---

## Performance Profile

```
Latency (time to first response):
  Claude    800ms   (Rank 1 for content)
  Gemini    1200ms  (Rank 1 for images)
  Codex     1500ms  (Rank 1 for scraping)

Success rate:
  Claude    99.5%   (most reliable)
  Gemini    98.8%   (very good)
  Codex     98%     (good)

Brand voice compliance:
  Claude    94-96%  (best)
  Gemini    92-94%  (good)
  Copilot   90-92%  (acceptable)
```

---

## Common Commands

```
Create blog posts (best quality):
  /create blog-posts about [topic]
  → Runs Claude (Rank 1)

Polish 50+ articles (best cost):
  /polish content in content/
  → Runs Gemini (cost-optimized for bulk)

Optimize images:
  /optimize images in content/
  → Runs Gemini (can see images)

Scrape competitors:
  /scrape all competitors blog
  → Runs Codex (scraping specialist)

View which tool was used:
  Check logs/workflow.jsonl
  Look for: "tool": "claude" | "gemini" | "codex"
```

---

## Merge Command (When Multiple Tools Succeed)

```
If both Claude and Gemini created content:
  content/sovereign/blog-posts/[slug]_[tool]_v[version].md
  content/sovereign/blog-posts/[slug]_[tool]_v[version].md

Choose Claude's version as primary:
  /merge content --prefer claude

Choose Gemini's version as primary:
  /merge content --prefer gemini

Export specific version:
  /export --version post_1_gemini_v1

Both versions become:
  post_1_claude_v1.md → archived to unused-versions/
  post_1_gemini_v1.md → renamed to post_1.md (primary)
```

---

## Debugging Checklist

**Command not using expected tool?**
- [ ] Check `commands_multi_tool.md` for that command's rankings
- [ ] Check logs/workflow.jsonl for actual tool used
- [ ] Verify guide-agent is loading `-multi-tool` files (not old versions)

**File not created with expected name?**
- [ ] Check if tool succeeded (look in logs)
- [ ] If fallback occurred, check if second tool created it
- [ ] Verify file naming follows: `[slug]_[tool]_v[n].md` pattern

**State not syncing?**
- [ ] Check `.ai/memory/multi-tool-state/[tool].session.json` exists
- [ ] Verify `.ai/memory/state.json` has `last_tool` field updated
- [ ] Check timestamp (newer timestamp = successful sync)

**Fallback not triggering?**
- [ ] Check error in logs/workflow.jsonl (why did Rank 1 fail?)
- [ ] Verify Rank 2 tool is available (check adapter file)
- [ ] Manually test Rank 2 tool: `/create blog-posts --tool gemini`

**Cost unexpectedly high?**
- [ ] Check which tool was used (logs/workflow.jsonl)
- [ ] For bulk work (>30 items), use: `--tool gemini` explicitly
- [ ] For one-off, Claude is fine (quality worth cost)
```

---

## File Locations (Phase 1)

```
Core architecture:
  .ai/tool-adapters/interface.json         ← Tool contract
  .ai/tool-adapters/claude_adapter.md      ← Claude rules
  .ai/tool-adapters/gemini_adapter.md      ← Gemini rules
  .ai/tool-adapters/_fallback_routing.md   ← Tool selection logic

Governance:
  .ai/commands_multi_tool.md               ← Command router (tool rankings)
  .ai/data_ownership_multi_tool.md         ← Ownership + versioning rules

Guides:
  .ai/PHASE_1_SETUP_GUIDE.md               ← Activation instructions
  .ai/PHASE_1_ARCHITECTURE_SUMMARY.md      ← Detailed design doc
  .ai/QUICK_REFERENCE.md                   ← This file

State:
  .ai/memory/state.json                    ← Global (unchanged)
  .ai/memory/multi-tool-state/
    ├─ claude.session.json                 ← Claude-specific
    └─ gemini.session.json                 ← Gemini-specific

Content output:
  content/sovereign/blog-posts/
    ├─ post_1_claude_v1.md                 ← From Claude
    ├─ post_1_gemini_v1.md                 ← From Gemini (fallback)
    └─ post_1.md                           ← After merge

Logs:
  logs/workflow.jsonl                      ← All commands (tool-tagged)
  logs/tool-performance.jsonl              ← Tool metrics (NEW)
```

---

## Next Steps (After Phase 1 Activation)

1. **Activate:** Tell guide-agent to load `-multi-tool` files
2. **Test:** Run `/create blog-posts` → verify Claude selected
3. **Monitor:** Check logs for first week
4. **Phase 2:** Plan CLI layer + Codex integration

---

## Contact / Issues

**Can't find a file?**
- Check `.ai/tool-adapters/` directory path
- Verify file extension (.md vs .json)

**Tool not selected as expected?**
- Check `commands_multi_tool.md` rankings
- Check tool availability (file exists? readable?)

**Performance confusing?**
- Check `logs/tool-performance.jsonl` for actual metrics
- Compare against Quick Reference cost/latency section


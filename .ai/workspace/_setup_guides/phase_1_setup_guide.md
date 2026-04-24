# Phase 1 Multi-Tool Implementation — Setup & Activation Guide
**Status:** ✅ Complete (Draft)  
**Date:** 2026-04-13  
**For:** Dorgham (Sovereign Workspace v3.2)

---

## What Phase 1 Delivers

**Two production-ready tool adapters:**
1. **Claude Adapter** — Primary tool; highest brand voice compliance
2. **Gemini Adapter** — Fallback + cost optimization; multimodal

**Five architectural files:**
1. `interface.json` — Canonical tool contract (all tools must implement)
2. `claude_adapter.md` — Claude's specific implementation
3. `gemini_adapter.md` — Gemini's specific implementation
4. `_fallback_routing.md` — Decision logic for tool selection + fallback chains
5. `commands_multi_tool.md` — Updated command router with tool rankings

**Two revised ownership/data files:**
1. `data_ownership_multi_tool.md` — File ownership rules for multi-tool world
2. (This guide)

---

## How It Works: Decision Tree

```
User: "/create blog-posts about sustainable design"
           ↓
     guide-agent parses command
           ↓
     Looks up in commands_multi_tool.md:
     - Rank 1: Claude
     - Rank 2: Gemini
     - Rank 3: Copilot
           ↓
     Attempts with Claude (Rank 1)
     ├─ Success? → Save to: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
     ├─ Timeout? → Fallback to Gemini → Save to: post_1_gemini_v1.md
     ├─ Originality <15%? → Retry with Gemini → Save to: post_1_gemini_v1.md
     └─ API error? → Fallback to Gemini
```

**Key difference from v3.2:**
- Old: Single tool (Claude); fail = stop
- New: Multiple tools; fail = retry with next tool; multiple outputs = user chooses

---

## Files Created (File Structure)

```
.ai/
├── tool-adapters/                    ← NEW DIRECTORY
│   ├── interface.json                ← Canonical contract (1.0.0)
│   ├── claude_adapter.md             ← Claude implementation
│   ├── gemini_adapter.md             ← Gemini implementation
│   ├── copilot_adapter.md            ← (Phase 2, planned)
│   ├── codex_adapter.md              ← (Phase 2, planned)
│   └── _fallback_routing.md          ← Tool selection logic
│
├── commands_multi_tool.md            ← REVISED (tool rankings added)
├── data_ownership_multi_tool.md      ← REVISED (tool-aware versioning)
│
└── (existing files unchanged)
    ├── agents.md
    ├── commands.md (kept for reference)
    ├── data_ownership.md (kept for reference)
    └── ...
```

---

## Key Architectural Decisions (Phase 1)

### 1. **Two-Tool Foundation (Claude + Gemini)**

**Why this pair?**
- Claude: Best reasoning, brand voice, most reliable (Rank 1 for content)
- Gemini: 5x cheaper, multimodal, 1M token context (fallback + image work)
- Together: Cover 80% of Sovereign's workloads with good cost/quality tradeoff

**Not included in Phase 1 (planned Phase 2+):**
- Codex — Code generation (scraping, automation)
- Copilot — IDE-native, CLI-friendly
- OpenCode — Code refactoring
- Kilo, Qwen — Lightweight/offline options
- Antigravity — Specialized IDE

---

### 2. **Tool Versioning (Not Global Versioning)**

**Old model (v3.2):**
- All content versioned globally: `post_1_v1.md` → `post_1_v2.md`
- Single tool; single output per command

**New model (Phase 1):**
- Content versioned **per tool**: `post_1_claude_v1.md` vs `post_1_gemini_v1.md`
- Multiple tools can output to same command; files coexist
- User chooses preferred version (or merges later with `/merge` command)

**Benefit:** Never lose a valid output. Compare quality across tools.

---

### 3. **Async + Fallback Execution**

**Sequential Fallback:**
```
/create blog-posts
  1. Try Claude (primary) → 4s, success
  2. (Gemini held as fallback)
  → Output: post_1_claude_v1.md
```

**If Claude fails (timeout, originality too low):**
```
/create blog-posts
  1. Try Claude (primary) → Timeout
  2. Fallback to Gemini (secondary) → 5s, success
  → Output: post_1_gemini_v1.md
  → Note: "Claude timed out; Gemini completed"
```

**If both fail:**
```
/create blog-posts
  1. Try Claude → Error
  2. Try Gemini → Error
  3. Try Copilot (Rank 3) → Success
  → Output: post_1_copilot_v1.md
  → Or: "All tools exhausted. Manual intervention required."
```

---

### 4. **Conflict Resolution Strategy: Version Branching**

**Scenario:** Claude and Gemini both complete successfully
```
content/sovereign/blog-posts/[slug]_[tool]_v[version].md  (Claude's output)
content/sovereign/blog-posts/[slug]_[tool]_v[version].md  (Gemini's output)
```

**Both kept.** User explicitly chooses:
```bash
/merge content --prefer claude     # Use Claude's version as primary
/merge content --prefer gemini     # Use Gemini's version as primary
/export                            # Export Claude's version (default)
/export --version post_1_gemini    # Export Gemini's version
```

---

### 5. **State Synchronization (Tool-Aware)**

**New state file:**
```
.ai/memory/multi-tool-state/
├── claude.session.json    ← Claude's tool-specific state
├── gemini.session.json    ← Gemini's tool-specific state
├── copilot.session.json   ← (Phase 2)
└── ...
```

**Global state remains:** `.ai/memory/state.json` (unchanged)

**Why separate?** Each tool has different context, limits, tokens. Tracking separately allows:
- Tool-specific token budgets
- Tool-specific error recovery
- Tool-specific performance metrics

---

## How to Activate Phase 1

### Step 1: Replace Command Router in guide-agent

**Current behavior:**
- guide-agent loads `.ai/commands.md` (Claude-only)

**New behavior:**
- guide-agent loads `.ai/commands_multi_tool.md` (Claude + Gemini + Copilot)
- Selects tool based on rank
- Passes request to correct adapter

**Action item:** Update guide-agent system prompt to:
```markdown
Load .ai/commands_multi_tool.md instead of .ai/commands.md
Check .ai/tool-adapters/[tool]-adapter.md for execution details
Follow fallback logic in .ai/tool-adapters/_fallback_routing.md
```

### Step 2: Initialize Tool-Specific State Files

**Create these files (can be empty initially):**
```bash
touch .ai/memory/multi-tool-state/claude.session.json
touch .ai/memory/multi-tool-state/gemini.session.json
```

**Sample content:**
```json
{
  "tool_id": "claude",
  "session_active": true,
  "last_command": null,
  "last_command_at": null,
  "tokens_used_this_session": 0,
  "context_loaded": []
}
```

### Step 3: Create Performance Tracking Log

**New file:** `logs/tool-performance.jsonl`

```json
{"timestamp": "2026-04-13T10:00:00+02:00", "tool": "claude", "command": "/brand", "duration_ms": 8500, "status": "success"}
{"timestamp": "2026-04-13T10:05:00+02:00", "tool": "gemini", "command": "/research competitors", "duration_ms": 3200, "status": "success"}
```

This log tracks tool performance over time and informs future ranking updates.

### Step 4: Update guide-agent Prompt

Add to guide-agent system prompt:

```markdown
## Multi-Tool Execution (Phase 1)

### Tool Selection
1. Read `commands_multi_tool.md` for command routing
2. Check tool rankings (Rank 1, 2, 3)
3. Load corresponding adapter (`.ai/tool-adapters/[tool]-adapter.md`)
4. Read tool-specific state: `.ai/memory/multi-tool-state/[tool].session.json`

### Fallback Execution
- If Rank 1 tool fails → Automatically try Rank 2 tool
- If Rank 2 fails → Try Rank 3 tool
- If all fail → Output error + log to `logs/workflow.jsonl`

### State Management
- After each command: Update both `.ai/memory/state.json` (global) and `.ai/memory/multi-tool-state/[tool].session.json` (tool-specific)
- Log command execution to `logs/workflow.jsonl` with `tool` field
- Log performance metrics to `logs/tool-performance.jsonl`

### Output Naming
- If Claude succeeds: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
- If fallback to Gemini: `content/sovereign/blog-posts/[slug]_[tool]_v[version].md`
- Both files coexist; user chooses via `/merge` or `--version` flag
```

---

## Quick Reference: Commands Now Have Tool Rankings

| Command | Rank 1 | Rank 2 | Rank 3 |
|---------|--------|--------|--------|
| `/brand` | Claude | Gemini | Copilot |
| `/research competitors` | Claude | Gemini | Codex |
| `/scrape *` | Codex | OpenCode | Claude |
| `/create blog-posts` | **Claude** | **Gemini** | Copilot |
| `/polish content` | Claude (≤30) / Gemini (>30) | Gemini / Claude | Copilot |
| `/optimize images` | **Gemini** | Claude | Codex |
| `/review` | Claude (tone) + Gemini (SEO parallel) | Claude | Manual |

**Key takeaway:** 
- Content creation → Claude first
- Image optimization → Gemini first
- Scraping → Codex first

---

## Testing Phase 1 (Recommended)

### Test 1: Basic Tool Selection
```bash
/create blog-posts about interior design
# Expected: Claude selected (Rank 1)
# Output: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
```

### Test 2: Cost-Optimized Fallback
```bash
/polish content in content/ --large-batch
# Expected: Gemini selected (cheaper for bulk)
# Output: Optimized in-place; log shows "tool: gemini"
```

### Test 3: Multimodal Priority
```bash
/optimize images in content/
# Expected: Gemini selected first (can see images)
# Output: content/assets-seo-[timestamp].json with Gemini-generated alt-text
```

### Test 4: Fallback Chain (Simulate)
```bash
/create blog-posts --force-fail-claude  # Simulates Claude timeout
# Expected: Fallback to Gemini
# Output: content/sovereign/blog-posts/[slug]_[tool]_v[version].md
# Log: tool_rank=2 (Gemini), fallback_reason="timeout"
```

---

## Known Limitations & Future Work

### Phase 1 Limitations
- ❌ No parallel execution (sequential only; one tool at a time)
- ❌ No advanced conflict resolution (user chooses manually)
- ❌ Only 2 tools (Claude + Gemini)
- ❌ No CLI wrappers yet (`sovereign-gemini`, `sovereign-claude`, etc.)

### Phase 2 Planned (Next)
- ✅ Add Codex + OpenCode for scraping/code generation
- ✅ Add Copilot for IDE-native workflows
- ✅ Implement CLI layer (`cli/sovereign`, `cli/sovereign-gemini`, etc.)
- ✅ Parallel execution mode (run Claude + Gemini simultaneously, compare results)
- ✅ Advanced conflict resolution (auto-merge logic based on quality gates)

### Phase 3 Planned (Later)
- ✅ Add Kilo + Qwen for lightweight/offline execution
- ✅ Add Antigravity IDE support
- ✅ Implement adaptive ranking (monthly performance reviews)
- ✅ Cost optimization features (`--cost-optimized` flag)

---

## Files to Keep / Files to Archive

### Keep (Production Use)
- ✅ `.ai/tool-adapters/interface.json` — Core contract
- ✅ `.ai/tool-adapters/claude_adapter.md` — In use
- ✅ `.ai/tool-adapters/gemini_adapter.md` — In use
- ✅ `.ai/tool-adapters/_fallback_routing.md` — In use
- ✅ `.ai/commands_multi_tool.md` — New primary commands file
- ✅ `.ai/data_ownership_multi_tool.md` — New ownership rules

### Archive (Reference Only)
- 📦 `.ai/commands.md` → Move to `.ai/archive/commands_v3.2.0.md`
- 📦 `.ai/data_ownership.md` → Move to `.ai/archive/data-ownership_v3.2.0.md`

### Update guide-agent Context
- Ensure guide-agent loads **-multi-tool** versions, not original versions

---

## Migration Checklist

- [ ] Create `.ai/tool-adapters/` directory
- [ ] Place all 5 adapter files in the directory
- [ ] Create `.ai/memory/multi-tool-state/` directory
- [ ] Initialize claude.session.json + gemini.session.json
- [ ] Create `logs/tool-performance.jsonl` (empty file to start)
- [ ] Update guide-agent system prompt (add Multi-Tool section)
- [ ] Test `/create blog-posts` → confirm Claude selected
- [ ] Test `/optimize images` → confirm Gemini selected
- [ ] Archive old `commands.md` and `data_ownership.md` to `.ai/archive/`
- [ ] Update CLAUDE.md manifest to reference new files

---

## Support & Questions

**If guide-agent can't find adapters:**
- Check `.ai/tool-adapters/` directory exists
- Verify file paths in commands_multi_tool.md match actual paths
- Check guide-agent has read permission

**If state not syncing:**
- Verify `.ai/memory/multi-tool-state/` directory exists
- Check `.ai/memory/multi-tool-state/[tool].session.json` files are readable
- Review state write logic in specific adapter files

**If fallback not triggering:**
- Check `_fallback_routing.md` for the specific command
- Verify error handling in adapter is implemented
- Check logs to see actual error (check `logs/workflow.jsonl`)

---

## Version & Maintenance

**Phase 1 Version:** 1.0.0  
**Last Updated:** 2026-04-13  
**Maintained by:** guide-agent (with fallback to manual review)

**To upgrade adapters (Phase 2):**
1. Add new adapter file to `.ai/tool-adapters/`
2. Update `interface.json` with new tool spec
3. Update `commands_multi_tool.md` with new rankings
4. Test with new tool; log performance
5. Increment Phase to 2.0.0

---

## Next Steps (Immediate)

1. ✅ **Activate:** Update guide-agent to load `-multi-tool` files
2. ✅ **Test:** Run 3-4 commands; verify tool selection + fallback
3. ✅ **Monitor:** Track `logs/tool-performance.jsonl` for first week
4. ⏭️ **Plan Phase 2:** Design CLI layer + Codex integration


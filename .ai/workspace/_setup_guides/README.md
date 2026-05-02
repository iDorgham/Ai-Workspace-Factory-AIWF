# _setup-guides/ — Quick Start & Implementation

**Purpose:** Get the workspace running, integrate new tools, onboard team members

Start here when setting up a new session or environment.

---

## 🚀 Setup Checklist

| Step | File | Time | Purpose |
|------|------|------|---------|
| 1 | `IMPLEMENTATION_CHECKLIST.md` | 15 min | Phase activation checklist |
| 2 | `PHASE_1_SETUP_GUIDE.md` | 10 min | Enable multi-tool support |
| 3 | `GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM.md` | 5 min | Update Claude system prompt |
| 4 | `GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM_PHASE2A.md` | 5 min | Enable CLI layer |
| **Total** | | **35 min** | Full workspace ready |

---

## 📄 Documents

### `IMPLEMENTATION_CHECKLIST.md`
**What:** Phase activation checklist  
**When:** Before using any new phase features  
**Action:** Go through checklist, check off each item  
**Success:** All items checked, workspace ready

### `PHASE_1_SETUP_GUIDE.md`
**What:** Multi-tool orchestration setup  
**When:** First time using Claude, Gemini, Copilot, etc. together  
**Action:** Follow integration steps, validate tools work  
**Success:** All tools available and responding

### `GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM.md`
**What:** Guide-agent system prompt extension  
**When:** Claude Code or Cowork system prompt needs updating  
**Action:** Append to Claude's system prompt  
**Success:** Claude recognizes all commands and agents

### `GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM_PHASE2A.md`
**What:** CLI layer system prompt  
**When:** Need to enable flag parsing (`--tool`, `--explain-routing`, etc.)  
**Action:** Append to system prompt AFTER main addendum  
**Success:** CLI flags recognized and parsed correctly

---

## 🎯 Common Scenarios

### New Session, First Time
1. Read `IMPLEMENTATION_CHECKLIST.md` (2 min)
2. Check prerequisites and activate features
3. Run verification command
4. **Ready to use!**

### Adding a New Tool (e.g., Qwen)
1. Reference `PHASE_1_SETUP_GUIDE.md` (tool integration section)
2. Add tool adapter in `../04-tool-adapters/`
3. Update `tool-registry.json`
4. Update `commands.md` with rankings
5. Run tests in `../08-testing/`
6. Done!

### Onboarding a New Team Member
1. Have them read `IMPLEMENTATION_CHECKLIST.md` (overview)
2. Walk through `PHASE_1_SETUP_GUIDE.md` together
3. Show them the workspace structure in root `README.md`
4. Point to `../06-brand-reference/` for brand voice training
5. Point to `.ai/templates/` for content blueprints
6. They're ready to create!

### Integrating into Existing Codebase
1. Copy `GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM.md` content
2. Append to your system prompt
3. For CLI features, also append `GUIDE_AGENT_SYSTEM_PROMPT_ADDENDUM_PHASE2A.md`
4. Test with sample command
5. Validate all agents recognized

---

## 📋 Pre-Setup Requirements

Before running through guides, ensure you have:

- [ ] Sovereign workspace folder created
- [ ] Access to at least one AI tool (Claude minimum)
- [ ] Brand positioning filled in (`../06-brand-content/sovereign/reference/market_positioning.md`)
- [ ] Content templates reviewed (`.ai/templates/`)
- [ ] 30 minutes for full setup

---

## ✅ Verification Commands

After setup, test with these commands:

```bash
# Test 1: Check system readiness
/budget check

# Test 2: List available agents
/memory load

# Test 3: Test CLI flags (Phase 2a)
/create blog-posts --explain-routing

# Test 4: Test tool selection
/create blog-posts --tool claude

# Test 5: Test parallel execution
/create blog-posts --parallel
```

All should succeed without errors.

---

## 🔗 Related Documents

- **Root `CLAUDE.md`** — Complete system reference (read after setup)
- **`../01-system-architecture/`** — Detailed architecture (optional deep dive)
- **`../02-agent-contracts/`** — Agent definitions (reference as needed)
- **`../03-cli-layer/`** — CLI documentation (for advanced flag usage)

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Agent not recognized" | Append system prompt addendum (see steps above) |
| CLI flags not working | Append Phase2A addendum after main one |
| Tool not available | Check `../04-tool-adapters/tool-registry.json` |
| Commands not routing | Review `../03-cli-layer/tool_router.md` |
| Permission denied on file | Check `../02-agent-contracts/data_ownership_multi_tool.md` |

---

## 📝 Notes

- Guides are sequential — don't skip steps
- Setup takes ~30 minutes one time
- After setup, workspace is ready indefinitely
- Periodically review `IMPLEMENTATION_CHECKLIST.md` for maintenance
- Update system prompt when adding new phases or agents

---

## 🚀 You're All Set!

After completing the setup guides, you can:
- ✅ Create content using `/create` commands
- ✅ Use multiple AI tools simultaneously
- ✅ Leverage CLI flags for advanced routing
- ✅ Manage multi-tool workflows
- ✅ Track and optimize tool usage

**Next:** Read `../README.md` for full workspace navigation.

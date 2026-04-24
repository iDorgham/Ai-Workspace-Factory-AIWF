# Command → Tool Routing Rules

Note: canonical executable source is `.ai/cli-layer/command-routing.json`.
Runtime implementation source is `.ai/scripts/tool_router_v2.py` (with `.ai/scripts/tool-router.py` compatibility shim).
This file is a human-readable mirror.

Registry references:
- Agent registry: `.ai/registry/agents.registry.json`
- Sub-agent registry: `.ai/registry/subagents.registry.json`
- Skill registry: `.ai/registry/skills.registry.json`
- Legacy compatibility maps: `.ai/compat/*.legacy-map.json`

**Purpose:** Map commands to optimal tool rankings based on command type and tool strengths

**Format:** Command type → [Rank 1, Rank 2, Rank 3, Rank 4+]

---

## Content Creation Commands

### /create blog-posts
- **Ranking:** Copilot > Codex > Gemini > Qwen
- **Optimization:** Quality over speed
- **Why Copilot:** Content quality matters most (94% brand voice)
- **Why Codex:** Fast, cheap, nearly same quality (91% brand voice)

### /create website pages
- **Ranking:** Copilot > Gemini > Codex > Qwen
- **Optimization:** Quality-balanced
- **Why Copilot:** Overall quality + brand alignment
- **Why Gemini:** Large context for complex structures

### /create landing pages
- **Ranking:** Copilot > Gemini > Codex > Qwen
- **Optimization:** Quality over speed
- **Why Copilot:** High-quality copy + branding critical

### /create project pages
- **Ranking:** Copilot > Codex > Gemini > Qwen
- **Optimization:** Quality + speed balance
- **Why Copilot:** Portfolio content quality important

---

## Content Optimization Commands

### /polish content
- **Ranking:** Copilot > Codex > Gemini > Qwen
- **Optimization:** Quality over speed
- **Why Copilot:** Refinement requires brand voice understanding (94%)

### /optimize images
- **Ranking:** Gemini > Codex > Copilot > Qwen
- **Optimization:** Multimodal required
- **Why Gemini:** Native image processing (1M context)
- **Why Codex:** Fast image optimization fallback

### /extract brand voice
- **Ranking:** Copilot > Gemini > Codex > Qwen
- **Optimization:** Quality over speed
- **Why Copilot:** Complex text analysis + nuance understanding

### /refine brand voice
- **Ranking:** Copilot > Gemini > Codex > Qwen
- **Optimization:** Quality over speed

---

## Analysis & Comparison Commands

### /research competitors
- **Ranking:** Gemini > Copilot > Codex > Qwen
- **Optimization:** Context over speed
- **Why Gemini:** Large context (1M tokens) for analyzing many competitors

### /scrape all competitors blog
- **Ranking:** Qwen > Codex > Copilot > Gemini
- **Optimization:** Speed + cost
- **Why Qwen:** Bulk processing, cheapest for large volumes

### /scrape all competitors projects
- **Ranking:** Qwen > Codex > Copilot > Gemini
- **Optimization:** Speed + cost

### /compare sovereign vs competitor
- **Ranking:** Gemini > Copilot > Codex > Qwen
- **Optimization:** Quality + context
- **Why Gemini:** Large context for detailed comparisons

### /intel competitor
- **Ranking:** Gemini > Copilot > Codex > Qwen
- **Optimization:** Context-heavy analysis
- **Why Gemini:** Best for multi-source synthesis across profile + scraped data

### /intel market snapshot
- **Ranking:** Gemini > Copilot > Codex > Qwen
- **Optimization:** Context over speed
- **Why Gemini:** Large-context pattern mining across many competitors

### /intel opportunities
- **Ranking:** Copilot > Gemini > Codex > Qwen
- **Optimization:** Decision quality
- **Why Copilot:** Stronger prioritization and recommendation narrative

---

## Administrative Commands

### /review
- **Ranking:** Copilot > Gemini > Codex > Qwen
- **Optimization:** Quality over speed

### /approve
- **Ranking:** Copilot > Codex > Gemini > Qwen
- **Optimization:** Quality over speed

### /export
- **Ranking:** Qwen > Codex > Copilot > Gemini
- **Optimization:** Speed + cost

### /archive old content
- **Ranking:** Qwen > Codex > Copilot > Gemini
- **Optimization:** Speed + cost

### /sync
- **Ranking:** Qwen > Codex > Copilot > Gemini
- **Optimization:** Speed + cost

---

## Fallback Strategies

### Quality-First (Default)
Pattern: Copilot > Codex > Gemini > Qwen
- Examples: /create *, /polish *, /extract *, /review, /approve
- Chain: Copilot (quality) → Codex (fast) → Gemini (context) → Qwen (fallback)

### Context-Heavy
Pattern: Gemini > Copilot > Codex > Qwen
- Examples: /research, /compare, /intel competitor, /intel market snapshot
- Chain: Gemini (1M context) → Copilot (quality) → Codex (fast) → Qwen (fallback)

### Decision-Scoring
Pattern: Copilot > Gemini > Codex > Qwen
- Examples: /intel opportunities
- Chain: Copilot (decision quality) → Gemini (context) → Codex (fast) → Qwen (fallback)

### Speed/Cost
Pattern: Qwen > Codex > Copilot > Gemini
- Examples: /scrape *, /export, /archive, /sync
- Chain: Qwen (cheap) → Codex (fast) → Copilot (quality) → Gemini (fallback)

### Multimodal
Pattern: Gemini > Codex > Copilot > Qwen
- Examples: /optimize images
- Chain: Gemini (native) → Codex (support) → others (fallback)

### Default (Unknown)
- Ranking: Copilot > Codex > Gemini > Qwen
- Reasoning: Most reliable general-purpose

---

**Version:** 1.0  
**Owner:** guide-agent  
**Updated:** 2026-04-13

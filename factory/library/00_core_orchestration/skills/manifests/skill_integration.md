# Sovereign Workspace — Skill Integration Map v3.2
# DEPRECATED MONOLITH NOTICE
# This document remains as a compatibility mirror.
# Canonical sources:
# - .ai/registry/skills.registry.json
# - .ai/skills/*/SKILL.md
# - .ai/compat/skills.legacy-map.json
# ============================================================
# Maps available Cowork skills to Sovereign workspace commands.
# guide-agent uses this to invoke the right skill for each command.
# Skills augment agent capabilities — they don't replace agent logic.
# ============================================================

---

## HOW SKILLS ARE INVOKED

When a Sovereign command maps to a Cowork skill:
1. guide-agent routes command to primary agent (as normal)
2. Primary agent invokes the mapped skill for the relevant sub-task
3. Skill output is passed back into the agent pipeline
4. Agent applies Sovereign-specific validation gates on top of skill output

Skills provide specialized capability modules. Agent contracts (`.ai/sub-agent-contracts.json`) define what's done with skill output.

---

## FULL SKILL MAPPING

### RESEARCH & COMPETITIVE INTELLIGENCE

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/research competitors` | `marketing:competitive-analysis` | research-agent / discovery-engine | Web discovery, relevance scoring, positioning gap identification |
| `/research competitors` | `marketing:competitive-brief` | research-agent / profile-builder | Structured competitor profiling: messaging, positioning, service comparison |
| `/compare sovereign vs competitor [name]` | `marketing:competitive-brief` | creator-agent / comparison-analyst | Side-by-side positioning, tone, and content diff report |
| `/compare sovereign vs competitor [name]` | `marketing:competitive-analysis` | creator-agent / comparison-analyst | Feature + messaging matrix comparison |

**Skill invocation notes:**
- `marketing:competitive-analysis` provides the raw competitive data layer
- `marketing:competitive-brief` generates the structured diff/comparison narrative
- After skill output: creator-agent validates originality ≤ 15%, applies Sovereign positioning lens

---

### MARKET INTELLIGENCE

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/intel competitor [name]` | `marketing:competitive-analysis` | research-agent / trend-miner | Build competitor-level signal extraction from profile + scraped corpus |
| `/intel competitor [name]` | `marketing:competitive-brief` | research-agent / intel-synthesizer | Produce concise strategic brief and actionable positioning insights |
| `/intel market snapshot` | `marketing:competitive-analysis` | research-agent / trend-miner | Identify cross-competitor market themes, topic concentration, and signal shifts |
| `/intel market snapshot` | `data:statistical-analysis` | research-agent / trend-miner | Quantify trend strength and evidence confidence across competitors |
| `/intel opportunities` | `data:statistical-analysis` | research-agent / opportunity-scorer | Score whitespace opportunities with confidence + risk bands |
| `/intel opportunities` | `marketing:competitive-brief` | research-agent / intel-synthesizer | Convert scoring output into operator-ready recommendations |
| `/intel opportunities` | `data:data-visualization` | research-agent / intel-synthesizer | Optional generation of matrix-style opportunity map summary for `content/sovereign/comparisons/opportunity-map-[timestamp].md` |

**Skill invocation notes:**
- Intelligence runs are additive and do not alter content approval gates.
- `trend-miner` must include confidence values; weak evidence outputs are flagged as `needs_more_data`.
- `opportunity-scorer` must provide rationale + suggested next command for each top opportunity.
- `intel-synthesizer` writes recommendations that chain into `/compare` or `/create` commands.

---

### CONTENT CREATION

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/create blog posts about [topic]` | `marketing:content-creation` | creator-agent / content-generator | Draft generation with SEO structure, keyword integration |
| `/create website pages` | `marketing:content-creation` | creator-agent / content-generator | Core page copy (Home, About, Services, Contact, FAQ) |
| `/create landing pages for [campaign]` | `marketing:campaign-planning` | creator-agent / blueprint-architect | Campaign brief + conversion-focused structure |
| `/create landing pages for [campaign]` | `marketing:content-creation` | creator-agent / content-generator | Landing page copy generation |
| `/create project pages` | `marketing:content-creation` | creator-agent / content-generator | Portfolio case study narrative |
| `/revise [feedback]` | `marketing:content-creation` | creator-agent / content-generator | Revised draft based on specific feedback |

**Skill invocation notes:**
- Skill drafts are ALWAYS passed through `brand-voice-applier` (tone ≥ 92%)
- Skill drafts are ALWAYS checked for originality ≤ 15% before saving
- Template blueprint from `.ai/templates/content-blueprints/[type].md` must be loaded before skill invocation to constrain structure

---

### BRAND DISCOVERY & VOICE

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/brand` | `brand-voice:guideline-generation` | brand-agent / brand-consultant | Optional augmentation: after interview answers collected, skill synthesizes patterns into structured guidelines before brand-consultant writes output files |
| `/brand` | `brand-voice:brand-voice-enforcement` | brand-agent / brand-consultant | Post-generation validation: checks that generated style_rules.md is internally consistent and enforceable |
| `/brand workshop` | `brand-voice:guideline-generation` | brand-agent / brand-interviewer + brand-synthesizer | Meeting-mode alias of `/brand`; synthesizes interview decisions into enforceable voice system |
| `/brand workshop` | `marketing:brand-review` | brand-agent / brand-governance-checker | Cross-checks workshop outputs for consistency and practical writing guidance |
| `/extract brand voice from [source]` | `marketing:brand-voice` | brand-agent / tone-analyzer | Tone extraction, lexical profiling, CTA style analysis |
| `/extract brand voice from [source]` | `brand-voice:guideline-generation` | brand-agent / tone-analyzer | Alternative: generate structured guidelines from source text |
| `/refine brand voice` | `marketing:brand-voice` | brand-agent / drift-detector + rule-updater | Drift detection against existing rules; rule update recommendations |
| `/review` (brand gate) | `marketing:brand-review` | workflow-agent / quality-checker | Brand voice compliance scoring against `style_rules.md` |
| `/review` (brand gate) | `brand-voice:brand-voice-enforcement` | workflow-agent / quality-checker | Enforcement scoring when brand-voice plugin is connected |
| `/polish content in content/` (brand pass) | `marketing:brand-review` | seo-agent + brand-agent | Voice compliance check as part of polish pipeline |

**Skill invocation notes:**
- `/brand` runs `brand-consultant` CLI interview FIRST — skill is invoked during synthesis, not before
- `brand-voice:guideline-generation` is the strongest skill for `/brand` post-processing — it understands brand document structure
- `marketing:brand-voice` extracts general tone patterns — brand-agent applies Sovereign-specific rules on top
- Brand gate in `/review` uses `marketing:brand-review` against `content/sovereign/reference/brand-voice/style_rules.md` as the rubric
- Threshold: ≥ 92% compliance required; skill score feeds into `quality-report.json`

---

### SEO OPTIMIZATION

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/polish content in content/` | `marketing:seo-audit` | seo-agent / keyword-auditor + technical-auditor | Keyword density, heading structure, meta generation, readability scoring |
| `/optimize images in content/` | `marketing:seo-audit` | seo-agent / image-seo-auditor | Image alt-text audit, accessibility check component |
| `/review` (SEO gate) | `marketing:seo-audit` | workflow-agent / quality-checker | SEO score ≥ 85% validation |

**Skill invocation notes:**
- `marketing:seo-audit` provides the SEO scoring layer
- seo-agent applies Sovereign-specific keyword map (`content/sovereign/_references/keyword_maps.md`) as the keyword source
- Technical auditor cross-references with `.ai/templates/seo-meta-templates/meta-template.json` schema

---

### CAMPAIGN PLANNING

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/create landing pages for [campaign]` | `marketing:campaign-planning` | creator-agent / blueprint-architect | Campaign brief: objectives, audience, channel strategy, success metrics |

**Skill invocation notes:**
- Campaign brief outputs inform landing page structure and CTA strategy
- Brief is saved to `content/sovereign/landing-pages/[campaign]-[slug].md[campaign]-brief.md` as reference (AI-only)

---

### WORKSPACE AUDITS & DOCS HEALTH

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/audit workspace` | `workspace:audit-orchestrator` | workflow-agent | Orchestrates recurring audit runs, consolidates pass/fail results, and emits health reports |
| `/audit docs` | `docs:lint-link-check` | workflow-agent / quality-checker | Runs local link checks, required file checks, stale marker checks, and mirror drift checks |
| `/report workspace health` | `workspace:audit-orchestrator` | workflow-agent | Generates summary report from canonical `.ai/workspace/status.json` and `.ai/workspace/index.json` |

**Skill invocation notes:**
- `workspace:audit-orchestrator` owns cadence + reporting orchestration only.
- `docs:lint-link-check` owns docs verification rules and check execution only.
- Both skills run under `workflow-agent` to avoid adding thin new agents.

---

### MEMORY & SESSION MANAGEMENT

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/memory save` | `productivity:memory-management` | guide-agent / memory-manager | Compress session context, update context-cache/ |
| `/memory load` | `productivity:memory-management` | guide-agent / memory-manager | Restore session context from context-cache/ |
| `/memory clear` | `productivity:memory-management` | guide-agent / memory-manager | Clear temp context, reset active session state |
| `/budget check` | `productivity:memory-management` | guide-agent | Token budget tracking, context size reporting |

**Skill invocation notes:**
- Memory skill manages the two-tier system: CLAUDE.md for working memory, `.ai/memory/` for full knowledge base
- Raw scraped files are NEVER included in memory save — summaries and pointers only

---

### WORKFLOW & QUALITY

| Sovereign Command | Cowork Skill | Invoked By | How Used |
|-----------------|-------------|------------|---------|
| `/review` | `marketing:brand-review` | workflow-agent / quality-checker (brand gate) | Brand voice compliance scoring |
| `/review` | `marketing:seo-audit` | workflow-agent / quality-checker (SEO gate) | SEO score calculation |
| Reporting & dashboards | `data:interactive-dashboard-builder` | guide-agent (on request) | Build HTML dashboard from sync logs, quality reports |
| Workspace documentation | `engineering:documentation` | guide-agent (on request) | Technical docs for scripts, agent contracts |

---

### DESIGN ALIGNMENT (for brand/design persona)

| Sovereign Use Case | Cowork Skill | Invoked By | How Used |
|------------------|-------------|------------|---------|
| Design critique of competitor layouts | `design:critique` | creator-agent / comparison-analyst | Structural and visual hierarchy diff vs. Sovereign |
| UX copy review | `design:ux-copy` | brand-agent | Review and refine CTA copy, navigation labels, form labels |
| Accessibility check on generated pages | `design:accessibility` | seo-agent / image-seo-auditor | WCAG AA compliance for generated content |
| Design system alignment | `design:design-system` | brand-agent | Ensure content references align with Sovereign's visual design system |

---

## SKILLS NOT CURRENTLY MAPPED (available but no current command)

| Skill | Potential Future Use |
|-------|---------------------|
| `marketing:email-sequence` | Future: `/create email sequence for [campaign]` command |
| `marketing:performance-analytics` | Future: `/analyse content performance` command |
| `marketing:performance-report` | Future: `/export performance report` command |
| `data:statistical-analysis` | Future: Competitor cadence analysis, keyword trend stats |
| `data:data-visualization` | Future: Visual reports on sync delta, content gaps |
| `engineering:code-review` | Future: Review generated Python scripts for quality |
| `engineering:system-design` | Future: Architecture decisions for workspace scaling |
| `product-management:roadmap-management` | Future: `/update roadmap` for workspace feature planning |
| `design:user-research` | Future: Client research synthesis for brief development |
| `design:design-handoff` | Future: Design specs for content layout hand-off to dev |

---

## SKILL INVOCATION PROTOCOL

When invoking a Cowork skill inside a Sovereign command flow:

```
1. Load required context (brand voice, positioning, keyword map)
2. Invoke skill with scoped input (not full workspace context)
3. Receive skill output
4. Apply Sovereign-specific validation:
   - Originality check (≤ 15% similarity)
   - Brand voice check (≥ 92%)
   - SEO check (≥ 85%)
5. If validation fails: retry with adjusted parameters (max 2x)
6. Save validated output to correct owned directory
7. Log to workflow.jsonl
```

**Rule:** Skills augment. Sovereign quality gates always run last.

---

*Last updated: 2026-04-14*
*Owner: guide-agent*

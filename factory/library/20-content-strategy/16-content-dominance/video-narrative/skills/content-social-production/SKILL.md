---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# Content & Social Production Engine

## Purpose

Plan, produce, and distribute content at scale across blog, email, social, and video channels — with concrete templates, calendars, and workflows for MENA bilingual markets. Replaces 6 thin skeleton stubs with one production-ready system.

**Consolidates:** `content/blog-calendar`, `content/video-script`, `content/email-sequence`, `content/social-matrix`, `social/engagement-plan`, `social/platform-playbook`

---

## Technique 1 — Content Calendar Architecture

### Monthly Calendar Template

```markdown
## Monthly Content Calendar

| Week | Blog (1×) | Email (2×) | LinkedIn (5×) | Instagram (5×) | TikTok (3×) |
|------|-----------|------------|---------------|----------------|-------------|
| W1 | Pillar article (SEO) | Welcome series #4 | Insight + data | Reel: tip | Behind-scenes |
| W2 | Cluster post | Newsletter | Case study | Carousel: how-to | Trending hook |
| W3 | Guest post / PR | Product update | Hot take | Story: poll | Product demo |
| W4 | Cluster post | Offer/promo | Weekly recap | Reel: result | Customer story |

## Content Pillar Categories (pick 3-4 per brand)
1. Educational: "How to solve [problem]" — builds authority
2. Proof: Customer stories, case studies, metrics — builds trust
3. Culture: Team, behind-scenes, values — builds connection
4. Product: Feature spotlights, demos, use cases — drives conversion
5. Industry: Trends, news, commentary — builds thought leadership

## MENA Calendar Overlay
- Ramadan: Switch to spiritual/family/giving themes (30 days)
- Eid: Celebration content + gift guides (3-5 days)
- National Days: Patriotic themes (UAE Dec 2, KSA Sep 23)
- White Friday: Sales-focused content (late Nov)
- Summer (Jul-Aug): Lighter content, many GCC residents travel
```

### Blog Post Production Template

```markdown
## Blog Post Brief (Fill before writing)

Title: [SEO-optimized, 50-60 chars]
Primary keyword: [from keyword cluster]
Secondary keywords: [3-5 related terms]
Search intent: Informational / Commercial / Transactional
Target word count: [Based on SERP analysis, typically 1,500-3,000]
Competitor URLs: [Top 3 ranking pages to beat]
Unique angle: [What we cover that competitors don't]
CTA: [What reader should do after reading]
Internal links: [3-5 existing pages to link to]
Author: [For E-E-A-T credibility]

## Post Structure
1. Hook (50 words): Problem statement or surprising stat
2. Context (100 words): Why this matters now
3. Meat (1,000-2,000 words): Solution/guide/analysis with H2/H3 sections
4. Examples (200 words): Real-world application, case study snippet
5. Takeaways (100 words): 3-5 bullet summary
6. CTA (50 words): One clear next action
7. FAQ schema (3-5 questions): For rich snippet opportunity
```

---

## Technique 2 — Email Production System

### Email Types & Templates

```markdown
## Email Type Library

### Transactional (triggered by user action)
- Welcome: Immediately on signup — deliver lead magnet + quick win
- Order confirm: Immediately — receipt + next steps + upsell
- Cart abandon: 1h / 24h / 72h sequence (3 emails)
- Review request: 7 days post-purchase — NPS + review link

### Nurture (automated drip)
- Welcome series: 7 emails over 21 days (see Growth Funnel skill)
- Re-engagement: For 90-day inactive — "We miss you" + incentive
- Milestone: Monthly/quarterly usage summary + tips

### Broadcast (manual send)
- Newsletter: Weekly/biweekly — curated insights + product updates
- Announcement: Product launch, feature release, company news
- Promotional: Flash sale, seasonal offer (Ramadan, Eid, White Friday)

## Email Copy Formula (AIDA)
Subject line: [Curiosity OR benefit OR urgency — max 50 chars]
Preview text: [Extend subject — don't repeat it — max 90 chars]
Body:
  Attention: Opening hook (stat, question, bold claim)
  Interest: "Here's why this matters for you..."
  Desire: Specific benefit / social proof / results
  Action: Single CTA button (high contrast, action verb)

## MENA Email Rules
- Arabic subject lines: 30% higher open rate in GCC vs English
- Send time (GCC): Tue-Wed-Thu, 10:00-12:00 local; Ramadan: after Iftar
- Formatting: RTL support in email template mandatory
- Unsubscribe: Arabic unsubscribe link in footer (compliance + UX)
```

---

## Technique 3 — Social Media Platform Strategy

### Platform-Specific Playbooks

```markdown
## LinkedIn (B2B — UAE/Saudi priority)
Posting cadence: 5×/week (Mon-Fri)
Best content types:
  1. Text-only posts with bold opening line (highest organic reach)
  2. Document posts (PDF carousel) — 3-5× more impressions
  3. Video: 60-90s, talking head with captions
  4. Polls: High engagement, useful for market research
Voice: Professional but human. Share opinions. Use "I" not "we".
Arabic: Optional for LinkedIn (English-dominant in GCC B2B)

## Instagram (B2C + Brand — UAE/Saudi)
Posting cadence: 5×/week (3 Reels, 1 Carousel, 1 Story series)
Best content types:
  1. Reels: 15-30s, trending audio, text overlay, Arabic subtitles
  2. Carousels: 5-10 slides, educational "swipe-to-learn"
  3. Stories: Polls, quizzes, behind-scenes (24h engagement boost)
Arabic: Arabic captions mandatory for KSA/EGY audiences
Hashtags: 5-10 relevant (mix of English + Arabic hashtags for MENA)

## TikTok (B2C — KSA priority, UAE growing)
Posting cadence: 3-5×/week
Content rules:
  - First 1.5 seconds: MUST hook (movement + text + sound)
  - Duration: 7-30s for awareness; 30-60s for tutorials
  - Arabic voiceover: 2-3× higher completion rate in KSA
  - Trend-jacking: Use Arabic viral sounds when appropriate
  - Creator content outperforms brand content by 3-5×

## Snapchat (KSA MANDATORY — 60%+ penetration)
  - Best for: Consumer brands, events, local businesses in KSA
  - Story format: 10-15 snaps telling a narrative
  - Discover: Partner with Snapchat Discover for mass reach

## X/Twitter (Growing in MENA tech community)
Posting cadence: 5-10×/week
  - Best for: Tech commentary, founder content, news reactability
  - Arabic tech Twitter growing rapidly in KSA
```

### Social Engagement System

```markdown
## Daily Engagement Protocol

Morning routine (15 min):
  □ Reply to ALL comments on posts from last 24h
  □ DM anyone who shared our content (thank + relationship)
  □ Like/comment on 10 posts from target audience
  □ Like/comment on 5 posts from industry influencers

Response time targets:
  - DM/comment: < 2 hours during business hours
  - WhatsApp: < 1 hour during business hours
  - Negative comment: < 30 minutes (damage control priority)
  - Review sites: < 24 hours (Google, Trustpilot, App Store)

Engagement rules:
  - NEVER: Ignore negative comments (always acknowledge, offer to help)
  - NEVER: Use generic responses ("Thanks for sharing! 🙏")
  - ALWAYS: Reference specific detail from their comment
  - ALWAYS: Ask a follow-up question to continue conversation
  - MENA: Reply in same language as commenter (Arabic→Arabic, English→English)
```

---

## Technique 4 — Video Script Framework

### Video Script Template

```markdown
## Short-Form Video Script (15-60s)

TARGET: Reels / TikTok / YouTube Shorts

HOOK (0-3s): [Pattern interrupt — what makes viewer STOP scrolling]
  Options: Bold claim / Surprising stat / "POV:" / "Stop doing X" / Question

SETUP (3-8s): [Context — why this matters]
  "Most [audience] make this mistake when..."
  "I tested [thing] for 30 days and here's what happened..."

BODY (8-45s): [Value delivery]
  Step 1 → Step 2 → Step 3 (3-step formula works best)
  OR: Problem → Discovery → Result (story arc)

CTA (45-60s): [What to do next]
  "Follow for more" / "Link in bio" / "Comment [keyword]"
  
PRODUCTION NOTES:
  - Text overlay: Essential for no-sound viewing (40%+ watch muted)
  - Captions: Arabic for KSA/EGY; English for LinkedIn
  - Aspect ratio: 9:16 (vertical) for Reels/TikTok/Shorts
  - Music: Use trending sounds within first 48h of trend
  - Lighting: Ring light or window light minimum (no dark/blurry)
```

---

## Anti-Pattern Catalog

| ID | Anti-Pattern | Risk | Fix |
|----|-------------|------|-----|
| CNT-001 | Publishing without a content calendar | **HIGH** — Inconsistent posting, gaps, burnout | Plan monthly calendar; batch produce weekly |
| CNT-002 | Same content across all platforms | **MEDIUM** — Each platform rewards different formats | Adapt format per platform (text→LinkedIn, Reel→IG/TikTok) |
| CNT-003 | English-only content for MENA audiences | **HIGH** — 40-60% lower engagement | Arabic version for KSA/EGY; bilingual for UAE |
| CNT-004 | Posting at wrong times for MENA | **MEDIUM** — Low visibility during off-hours | GCC best: 10-12 Sun-Thu; Ramadan: after Iftar |
| CNT-005 | No CTA in content | **MEDIUM** — Content drives awareness but not action | Every piece needs one clear CTA |
| CNT-006 | Video without captions/text overlay | **HIGH** — 40%+ watch muted, especially scrolling | Always add text overlay or captions |
| CNT-007 | Ignoring Snapchat for KSA campaigns | **HIGH** — Missing 60%+ of Saudi users | Snapchat mandatory for consumer brands in KSA |
| CNT-008 | Newsletter without segmentation | **MEDIUM** — Low relevance = high unsubscribes | Segment by: language, industry, engagement level |

## 🌍 Regional Calibration (MENA Context)

- **Cultural Alignment:** Ensure all logic respects regional business etiquette and MENA market expectations.
- **RTL Compliance:** Logic must explicitly handle Right-to-Left (RTL) flow where relevant.

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Generic Output -> *Correction:* Apply sector-specific professional rules from RULE.md.
- **Anti-Pattern:** Global-Only Logic -> *Correction:* Verify against MENA regional calibration.

---

## Success Criteria

- [ ] Monthly content calendar planned with all channels mapped
- [ ] Blog: 1 pillar + 2-4 cluster posts published per month
- [ ] Email: Welcome sequence (7 emails) + weekly newsletter active
- [ ] Social: Platform-specific content (not cross-posted) on 3+ channels
- [ ] Video: Minimum 3 short-form videos per week (Reels/TikTok)
- [ ] Engagement: All comments responded within 2 hours during business hours
- [ ] Arabic content produced for KSA/EGY audiences (not just translated)
- [ ] Content performance tracked weekly (views, engagement rate, click rate)
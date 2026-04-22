# TEMPLATE: Landing Page Blueprint
# ============================================================
# USED BY: creator-agent / blueprint-architect
# CONTENT TYPE: content/sovereign/landing-pages/
# AGENT RULE: Each landing page is campaign-specific.
#             Fill [CAMPAIGN] placeholders from user command.
# ============================================================

---
## FRONTMATTER

```yaml
---
title: "[Campaign-specific title — keyword-rich, ≤ 60 chars]"
meta_description: "[120–155 chars — value proposition + clear CTA]"
keywords:
  - "[primary campaign keyword]"
  - "[intent keyword]"
  - "[location keyword]"
slug: "[campaign-slug]"
content_type: "landing-page"
campaign: "[campaign name from /create landing pages for [campaign]]"
author: "Sovereign Studio"
created_at: "[ISO8601 timestamp]"
version: 1
status: "draft"
---
```

---

## STRUCTURE BLUEPRINT

### HERO SECTION
**Purpose:** Establish value proposition above the fold.  
**Length:** 25–40 words (headline + subline)  
**Tone:** Clear, confident, evocative. No generic taglines.

```
[H1: Primary benefit statement — what the client receives]
[Subheadline: Specific context — who this is for, what makes it different]
[Hero CTA Button: Single, specific action]
```

Examples:
> H1: "A Space Designed Around Your Life, Not Around a Trend"  
> Sub: "Sovereign accepts residential commissions in Cairo and Dubai. We begin with a conversation."  
> CTA: "Begin a conversation →"

---

### TRUST SECTION — Proof before pitch
**Purpose:** Establish credibility immediately. Not a wall of text — 3 specific proof points.  
**Length:** 30–50 words total (3 × 10–15 words)  
**Format:** 3-column layout with icon or number

```
[Proof 1]: [Specific credential — years, commissions, or notable fact]
[Proof 2]: [Process differentiator — e.g., "Each commission receives exclusive focus for 6 months"]
[Proof 3]: [Value differentiator — e.g., "Materials sourced from 12 European ateliers"]
```

---

### CAMPAIGN-SPECIFIC CONTENT BLOCK
**Purpose:** Explain what this campaign/service is about in depth.  
**Length:** 150–250 words  
**Tone:** Specific, benefit-oriented, no filler.

> *[Explain what is being offered in this campaign. Be specific about scope, timeline, and what the client experience looks like. Connect it to a problem the client has.]*

---

### VISUAL PROOF SECTION — Portfolio reference
**Purpose:** Let the work speak. Minimum 3 project references.  
**Format:** Image + project name + 1-sentence descriptor

```
[Project image]
[Project Name] — [City, Year]
"[One sentence on what made this commission distinctive]"
```

---

### PROCESS SECTION — Remove the unknown
**Purpose:** Show the client what working with Sovereign looks like, step by step. Reduce friction.  
**Length:** 4–5 steps, 20–40 words each.

```
Step 1: The Conversation
[What happens, what the client needs to bring, what they'll walk away with]

Step 2: The Vision
[...]

Step 3: The Design
[...]

Step 4: The Commission
[...]

Step 5: The Space
[The handover experience]
```

---

### OBJECTION HANDLING (optional, use when campaign targets high-consideration decision)
**Purpose:** Address 2–3 likely hesitations directly, without being defensive.  
**Format:** Question + short, confident answer.

```
"How long does a commission take?"
[Honest, specific answer]

"Do you work with clients outside Cairo?"
[...]

"What's the minimum project scope?"
[...]
```

---

### FINAL CTA SECTION
**Purpose:** One clear next action. No choice overload.  
**Length:** 30–60 words  
**Tone:** Warm invitation, not pressure.

```
[H2: One final resonant headline]
[1–2 sentences reinforcing the invitation]
[Single CTA button — same text as hero CTA for consistency]
[Secondary micro-copy: e.g., "No commitment. Just a conversation."]
```

---

## CONVERSION DESIGN NOTES (for design handoff)

- **Single CTA:** Same button copy used in hero and footer (consistency = trust)
- **No navigation:** Landing pages should suppress main nav to reduce exit opportunities
- **Form placement:** If contact form used, place after process section (trust established first)
- **Mobile-first:** Hero text must be legible at 320px width
- **Load speed:** Limit hero image to < 150KB (WebP, lazy-load below fold)

---

## SEO CHECKLIST

- [ ] H1 contains primary campaign keyword
- [ ] Meta description contains value proposition + CTA intent
- [ ] Page structured for long-tail intent (e.g., "interior designer Cairo consultation")
- [ ] All images optimized with alt-text
- [ ] No duplicate content from other Sovereign pages (unique angle required)

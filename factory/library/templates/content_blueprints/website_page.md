# TEMPLATE: Website Page Blueprint
# ============================================================
# USED BY: creator-agent / blueprint-architect
# CONTENT TYPE: content/sovereign/website-pages/
# PAGES: Home, About, Services, Contact, FAQ
# AGENT RULE: Each page has its own section variant below.
#             Select the variant matching the page being created.
# ============================================================

---
## FRONTMATTER

```yaml
---
title: "[Page Title — Primary Keyword, ≤ 60 chars]"
meta_description: "[120–155 chars — value proposition + location signal]"
keywords:
  - "[primary keyword]"
  - "[secondary keyword]"
  - "[location keyword]"
slug: "[page-name]"
content_type: "website-page"
page_type: "home | about | services | contact | faq"
author: "Sovereign Studio"
created_at: "[ISO8601 timestamp]"
version: 1
status: "draft"
---
```

---

## VARIANT A: HOME PAGE

**Purpose:** Establish Sovereign's identity and invite the right visitor to go deeper.  
**Tone:** Evocative, confident. This is a first impression — make it count.

### Hero Section
**Words:** 25–45  
**Format:** Headline + Subline + Single CTA

```
[H1: Primary value proposition — what Sovereign creates and for whom]
[Subline: Qualifying sentence — who this is for, what makes it singular]
[CTA: "Explore our work" or "Begin a conversation"]
```

### Introduction Section
**Words:** 80–120  
**Tone:** Studio voice — who we are and what we believe

> *[Two paragraphs. First: what Sovereign is. Second: what Sovereign believes. No features list. No service menu. Pure positioning.]*

### Work Preview (visual anchor)
**Words:** 3–5 per project  
**Format:** 3 selected projects, each with image + project name + city, year

```
[Project image]
[Project name] — [City, Year]
```

### Services Teaser
**Words:** 60–100  
**Format:** Brief intro + 3–4 named services + CTA to services page

> *[Introduce the range of work without listing everything. 3–4 service names with 1-line each. "See the full scope →"]*

### Trust Indicators
**Words:** 20–40  
**Format:** 3 specific proof points (not generic claims)

```
[Number or fact that signals scale/quality]
[Process differentiator]
[Geographic or niche signal]
```

### Closing CTA
**Words:** 30–50  
**Tone:** Invitation, not pressure

> *[One final thought that resonates with the visitor. Single CTA button: "Begin a conversation" or "See our work"]*

---

## VARIANT B: ABOUT PAGE

**Purpose:** Build trust through story and philosophy. Who are the people behind the work?  
**Tone:** Personal, thoughtful, specific.

### Opening — The founding story
**Words:** 100–150  
**Tone:** First-person or close studio voice. Not a corporate bio.

> *[Why Sovereign was founded. The gap in the market it was created to fill. The belief that drives the work. Specific, not generic.]*

### Philosophy Section
**Words:** 120–180  
**H2: e.g., "How we work" or "What we believe"

> *[The design philosophy in 2–3 paragraphs. Connect it to real outcomes: how clients experience it, how the space feels afterward.]*

### Studio Profile (brief)
**Words:** 60–100  
**Format:** 2–3 sentences per key team member (if public-facing) or a collective studio description

> *[Who the studio is — background, training, experience — without reading like a CV. What they've done that's relevant to who a client would become.]*

### Values Section
**Words:** 80–120  
**Format:** 3–4 core values, each with name + 2-sentence elaboration

```
[Value name]
[2 sentences on what this means in practice, not in theory]
```

### Closing Invitation
**Words:** 40–60  
**CTA:** "If this sounds like the kind of care you're looking for →"

---

## VARIANT C: SERVICES PAGE

**Purpose:** Clearly define what Sovereign offers, who it's for, and what the process looks like.  
**Tone:** Clear, precise, benefit-oriented. Not a feature list.

### Opening
**Words:** 60–100  
**Tone:** Position the approach before listing services

> *[One paragraph on how Sovereign thinks about scope — not what services are offered yet, but why the services are structured as they are.]*

### Services (one per H2)
**Words:** 80–120 per service  
**Format:** Service name (H2) + What it includes + Who it's for + What the client receives

Repeat for each service:
```
## [Service Name]
[What this service encompasses]
[Who typically engages this service and why]
[What the outcome looks and feels like]
```

### Process Overview
**Words:** 100–150  
**Format:** 4–5 steps, 20–30 words each

```
### How a commission works
1. [Step 1 — name + what happens]
2. [Step 2...]
3. [Step 3...]
4. [Step 4...]
5. [Step 5 — handover]
```

### Closing CTA
**Words:** 30–50  
**CTA:** "Tell us about your space →" or "Begin a conversation →"

---

## VARIANT D: CONTACT PAGE

**Purpose:** Reduce friction to making contact. Build enough confidence to act.  
**Tone:** Warm, practical, specific.

### Opening
**Words:** 40–70  
**Tone:** Welcoming, no pressure

> *[What happens when someone reaches out. What the first conversation looks like. Reassure: no commitment, just a discussion.]*

### Contact Information Block
```
Studio address: [address]
Email: [email]
Phone: [phone, if public]
Social: [key platforms]
Studio hours: [hours + timezone]
```

### Contact Form Context (if form exists)
**Words:** 20–30  
**Format:** Short framing above the form

> *[One sentence on what information helps the conversation. Keep it light — not an interrogation.]*

### Location + Studio Visits
**Words:** 40–60  
**If studio visits are by appointment:** say so clearly

---

## VARIANT E: FAQ PAGE

**Purpose:** Reduce objections and answer the questions that appear before a first enquiry.  
**Tone:** Direct, honest, confident. Not defensive.

### Format Rules
- Q&A format ONLY on this page (exception to Rule S-05 — FAQ format for utility pages is permitted)
- Each answer: 40–80 words
- Questions should reflect real client hesitations, not marketing questions
- Group questions into 2–3 H2 themes

### Recommended Q&A Themes

**About the process:**
- How long does a commission take?
- What does the process look like, step by step?
- How involved do I need to be?

**About scope and investment:**
- What is the minimum scope you work on?
- Do you provide cost management?
- How are fees structured?

**About geography:**
- Do you work with clients outside [primary city]?
- Can we meet remotely?

**About the work:**
- Can I see examples of [specific type] projects?
- Do you work with a specific aesthetic or style?

### Closing Section
**Words:** 30–50  
**CTA:** "Still have questions? Let's talk →"

---

## SEO CHECKLIST (all variants)

- [ ] Primary keyword in H1 and meta description
- [ ] Location keyword present (for local SEO signal)
- [ ] Meta description 120–155 chars
- [ ] H-structure valid (one H1, logical H2/H3 hierarchy)
- [ ] No keyword stuffing (density ≤ 2%)
- [ ] Internal links to key pages (blog, projects, contact)
- [ ] All images have descriptive alt text
- [ ] Schema markup type: LocalBusiness or Service

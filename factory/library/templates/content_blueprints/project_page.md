# TEMPLATE: Project / Case Study Page Blueprint
# ============================================================
# USED BY: creator-agent / blueprint-architect
# CONTENT TYPE: content/sovereign/projects/
# AGENT RULE: Fill from actual project data when available.
#             If no project data exists, generate a placeholder structure
#             and flag with [NEEDS CLIENT DATA] for human review.
# ============================================================

---
## FRONTMATTER

```yaml
---
title: "[Project Name] — [City, Year]"
meta_description: "[120–155 chars: project type, location, key design decision]"
keywords:
  - "[project type + location keyword]"
  - "[material or style keyword]"
  - "[service keyword]"
slug: "[project-name-city-year]"
content_type: "project"
project_type: "residential | commercial | hospitality | mixed"
location: "[City, Country]"
year_completed: "[YYYY]"
scope: "[e.g., Full interior design, furniture procurement, art curation]"
author: "Sovereign Studio"
created_at: "[ISO8601 timestamp]"
version: 1
status: "draft"
---
```

---

## STRUCTURE BLUEPRINT

### SECTION 1: PROJECT IDENTITY — The brief in one breath
**Purpose:** Establish the project, the client's intent, the design challenge.  
**Length:** 80–120 words  
**Tone:** Considered, contextual. No "The client wanted X so we did Y" mechanical recounting.

> *[Describe the commission's essential character — not what was done, but what was being sought. Where was the tension? What was the question the space needed to answer?]*

**Field data needed:** Location, project type, brief summary, client intent (anonymised)

---

### SECTION 2: THE APPROACH — Design rationale
**Purpose:** Explain the thinking behind the design decisions. Not a list of features — a connected logic.  
**Length:** 150–250 words (2–3 paragraphs)  
**Tone:** Authoritative, process-oriented. Share the reasoning, not just the result.

> *[Walk through the key design decision and its rationale. Connect material choices, spatial decisions, and atmospheric goals into a coherent thread.]*

**Structure options:**
- H3: "The Material Logic" — why these specific finishes/materials
- H3: "The Light Strategy" — how light was considered
- H3: "The Spatial Sequence" — how the rooms relate to each other

---

### SECTION 3: KEY DECISIONS — 2–3 specific design choices
**Purpose:** Highlight the decisions that define this commission.  
**Length:** 80–120 words per highlight (total 200–350 words)  
**Format:** Each highlighted decision gets a short paragraph + image reference.

> *[For each key decision: what was chosen, where it came from, and why it serves the space. Specificity is essential — material origin, artisan, technique, or dimension if relevant.]*

Example structure:
```
#### [H4: The material name or decision name]
[2–3 sentences on the decision's logic and source]
![Alt text: descriptive + keyword-aware][image-ref]
```

---

### SECTION 4: THE RESULT — Lived-in language
**Purpose:** Describe the completed space as it is experienced, not as a technical outcome.  
**Length:** 100–150 words  
**Tone:** Evocative, sensory. The reader should feel the space, not just understand it.

> *[Write about the completed space from the perspective of being in it. What quality does it have now? How does it move, breathe, settle?]*

---

### SECTION 5: PROJECT CREDITS + CTA
**Purpose:** Transparency and next-step invitation.  
**Length:** Short (credits block + 1-sentence CTA)

```
**Studio:** Sovereign  
**Location:** [City, Country]  
**Year:** [YYYY]  
**Scope:** [Brief scope list]  
**Photography:** [Photographer name, if applicable]  
**Key Suppliers:** [List if permitted, otherwise omit]

[CTA] Begin a conversation about your space →
```

---

## IMAGE GALLERY GUIDE

| Image Slot | Content | Alt Text Pattern |
|-----------|---------|-----------------|
| Hero (full-width) | Most characteristic space | "[Room type] in [project name] — [primary material or quality]" |
| Detail 1 | Key material or finish | "[Material] detail — [location in space]" |
| Detail 2 | Light quality or proportion | "[Quality] — [specific design element]" |
| Lifestyle | Space in use or full-room composition | "[Room type] — [key design quality], [location]" |
| Exterior/Context (if applicable) | Building or entry | "[Project name] — [exterior descriptor], [city]" |

Minimum 4 images per project page.

---

## SEO CHECKLIST

- [ ] Primary keyword (project type + location) in title and first 100 words
- [ ] Meta description includes project type, location, and key differentiator
- [ ] Project location in H1 or prominent H2
- [ ] All images alt-text complete (descriptive + contextual)
- [ ] No keyword stuffing (density ≤ 2%)
- [ ] At least one internal link to related blog post or service page

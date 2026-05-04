<div align="center">

# Ezzat Gamaly — Photographer portfolio & CMS website

**Portfolio website development** for a professional photography practice, evolving toward a **content-managed** experience: curated galleries, strong performance with large media, clear editorial workflow, and a brand that reads as **premium and trustworthy** for clients and collaborators.

[![Portfolio](https://img.shields.io/badge/focus-portfolio%20%2B%20CMS-1a2332)](./ezzat-gamaly/001_portfolio-website/)
[![Docs](https://img.shields.io/badge/docs-hub-0366d6)](./ezzat-gamaly/001_portfolio-website/docs/README.md)
[![PRD](https://img.shields.io/badge/spec-PRD-6e7681)](./ezzat-gamaly/001_portfolio-website/docs/product/PRD.md)
[![Roadmap](https://img.shields.io/badge/plan-roadmap-30363d)](./ezzat-gamaly/001_portfolio-website/docs/product/ROADMAP.md)

</div>

---

## About this work

**Ezzat Gamaly** is a **photographer** building a public-facing **portfolio site** that will grow into **Ezzat Portfolio CMS**: the same product story, but with room for structured content, repeatable publishing, and long-term maintainability—not only static pages.

This README points contributors and reviewers to the **website development** story: who it serves, what “done” means for photography on the web, and where every product document lives. Implementation details, stack notes, and delivery checklists stay in **`docs/`** inside the project folder so the narrative stays next to the code.

---

## Table of contents

- [What we are building](#what-we-are-building)
- [Quality bar for a photography portfolio](#quality-bar-for-a-photography-portfolio)
- [Product vision (summary)](#product-vision-summary)
- [Documentation hub](#documentation-hub)
- [Project location](#project-location)
- [Open in your editor (workspace file)](#open-in-your-editor-workspace-file)
- [How we develop (high level)](#how-we-develop-high-level)

---

## What we are building

The active development tree is **`ezzat-gamaly/001_portfolio-website/`**. There you will find:

- The **website** (application code as the stack matures).
- **`docs/`** — human-written **product and delivery** documentation: context, PRD, roadmap, architecture and compliance notes where relevant, onboarding order, and playbooks for design and Git workflow.
- Planning and configuration that support **phased delivery** of the portfolio and CMS capabilities described in the PRD.

The **[Product Requirements Document](./ezzat-gamaly/001_portfolio-website/docs/product/PRD.md)** is the authoritative description of **Ezzat Portfolio CMS**: scope, principles, roadmap alignment, and acceptance thinking. Treat it as the single source of truth when prioritizing features for the **photography portfolio** and its editorial surface.

---

## Quality bar for a photography portfolio

A photographer’s site is judged in seconds. This project assumes:

- **Imagery first:** fast, respectful loading of large photos; layouts that let work breathe without clutter.
- **Accessibility:** meaningful alt text, legible type, sensible motion, keyboard-friendly patterns where interactive UI exists.
- **Performance on real networks:** especially mobile and variable connectivity common in regional markets.
- **Brand and language:** copy and structure that support **bilingual or localized** experiences when the product specs call for them—without diluting a premium visual identity.

These expectations are reflected in the PRD and supporting docs; they are the lens for **website** and **CMS** decisions alike.

---

## Product vision (summary)

The full vision lives in **[`docs/product/PRD.md`](./ezzat-gamaly/001_portfolio-website/docs/product/PRD.md)**. At a high level the product direction includes:

- A **sovereign, professional** portfolio experience suitable for **MENA** creators and studios, with data and compliance posture defined in product documentation—not as an afterthought.
- **Structured delivery:** requirements and phases are written down before large buildouts; C4-style architecture and contracts in the plan tree support clear handoffs between design, content, and engineering.
- **Traceable publishing** as the CMS matures: drafts, review, and publish paths that stay understandable for the photographer and stakeholders.

For **milestones and phases**, use **[`docs/product/ROADMAP.md`](./ezzat-gamaly/001_portfolio-website/docs/product/ROADMAP.md)**. For **Git branching, tags, and release habits**, use **[`docs/product/GIT_VERSIONING_BRANCHING_TAGS.md`](./ezzat-gamaly/001_portfolio-website/docs/product/GIT_VERSIONING_BRANCHING_TAGS.md)**.

---

## Documentation hub

All human-facing specs are indexed from **[`docs/README.md`](./ezzat-gamaly/001_portfolio-website/docs/README.md)**. Quick map:

| Area | Document | Role |
|------|----------|------|
| **Index** | [`docs/README.md`](./ezzat-gamaly/001_portfolio-website/docs/README.md) | Entry point to every doc |
| **Context** | [`docs/overview/CONTEXT.md`](./ezzat-gamaly/001_portfolio-website/docs/overview/CONTEXT.md) | Audience, goals, constraints |
| **PRD** | [`docs/product/PRD.md`](./ezzat-gamaly/001_portfolio-website/docs/product/PRD.md) | Scope for portfolio + CMS |
| **Roadmap** | [`docs/product/ROADMAP.md`](./ezzat-gamaly/001_portfolio-website/docs/product/ROADMAP.md) | Phases and delivery timeline |
| **Product folder** | [`docs/product/`](./ezzat-gamaly/001_portfolio-website/docs/product/) | Architecture, governance, readiness, compliance—see folder on GitHub |
| **Onboarding** | [`docs/guides/ONBOARDING.md`](./ezzat-gamaly/001_portfolio-website/docs/guides/ONBOARDING.md) | Recommended order: repo → design baseline → specs → planning |
| **Delivery playbooks** | [`docs/profile/README.md`](./ezzat-gamaly/001_portfolio-website/docs/profile/README.md) | Design onboarding, git workflow, hooks, recommendations |
| **Technical context** | [`docs/context/README.md`](./ezzat-gamaly/001_portfolio-website/docs/context/README.md) | Stack and ADRs—**no secrets** |

---

## Project location

| Path | What it is |
|------|------------|
| [`ezzat-gamaly/001_portfolio-website/`](./ezzat-gamaly/001_portfolio-website/) | **Website + docs + planning** — primary folder for day-to-day development |
| [`ezzat-gamaly/ezzat-gamaly-portfolio.code-workspace`](./ezzat-gamaly/ezzat-gamaly-portfolio.code-workspace) | Optional **multi-root** editor workspace (see next section) |

---

## Open in your editor (workspace file)

1. In **Cursor** or **VS Code**: **File → Open Workspace from File…**
2. Open **`workspaces/clients/ezzat-gamaly/ezzat-gamaly-portfolio.code-workspace`**

That file opens:

| Root | When to use it |
|------|----------------|
| **`001_portfolio-website`** | Default: edit the site, read `docs/`, and run project scripts from the website folder. |
| **Repository root (optional)** | Use when you also want the parent tree visible in the same window (e.g. shared assets or org-wide files). |

**Single-folder option:** open **`workspaces/clients/ezzat-gamaly/001_portfolio-website`** only if you prefer one root—everything important for the **portfolio CMS website** lives there.

---

## How we develop (high level)

Follow **[`docs/guides/ONBOARDING.md`](./ezzat-gamaly/001_portfolio-website/docs/guides/ONBOARDING.md)** for the agreed sequence: establish the **application repository** and Git practices, lock a **design baseline**, align **PRD / roadmap / context**, then expand **planning and specs** before large implementation passes.

Delivery expectations (regional posture, privacy, and release discipline) are spelled out in **`docs/product/`**—start from the PRD and the compliance or architecture documents linked from the docs index.

---

<div align="center">

**Ezzat Gamaly — Photography · Portfolio · CMS website development**

</div>

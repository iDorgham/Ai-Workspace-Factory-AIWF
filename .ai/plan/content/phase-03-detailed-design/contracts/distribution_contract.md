# Distribution Contract — Phase 03: Detailed Design
**Reasoning Hash:** sha256:aiwf-v21-launch-content-03-detailed-design-2026-04-25

---

## Channel Distribution Rules

### GitHub (C-01-README, C-12-GH-MENA)
- Publish via direct commit to main branch
- Commit message format: `docs(readme): {description} [Reasoning: sha256:{hash}]`
- README must render correctly in GitHub dark mode before publish
- Check: all Mermaid diagrams render, all links resolve, badges display

### LinkedIn (C-02-LI-LAUNCH, C-04-LI-12SPEC, C-06-LI-LAW151, C-07-AR-LI, C-10-LI-7CLI)
- Schedule via LinkedIn Creator Studio or manual post
- Link goes in first comment — NEVER in post body (LinkedIn suppresses reach)
- Maximum 3 hashtags per post
- Arabic post (C-07) must be posted in RTL context — verify mobile rendering

### X / Twitter (C-03-X-LAUNCH, C-05-X-ARCH, C-11-X-MULTILLL)
- Post threads manually or via Buffer/Typefully
- Thread posts must be published within 2 minutes of each other
- Post 1 of every thread must stand alone if separated from thread
- Architecture diagram (C-05) requires image alt text: "C4 context diagram showing AIWF Tripartite Planning architecture"

### Dev.to (C-09-DEVTO)
- Front matter required: title, tags (max 4), canonical_url, cover_image
- Canonical URL points to GitHub repo
- Cross-post to Hashnode 48 hours after Dev.to publish

### Arabic MENA Communities (C-08-AR-MENA)
- Distribute to: Arab Developers on Facebook, MENA AI Slack, local Telegram groups
- Post in Arabic only — no English fallback in same post
- Include GitHub link as plain URL (no link preview suppression in groups)

## Timing Rules

| Day | Pieces | Notes |
|-----|--------|-------|
| 1 | C-01, C-02, C-03 | GitHub first (08:00 Cairo), LinkedIn (10:00), X (12:00) |
| 3 | C-04 | LinkedIn optimal: Tue/Wed/Thu 09:00–11:00 Cairo |
| 5 | C-05 | X only — diagram post, no LinkedIn on same day |
| 7 | C-06, C-07, C-08 | English LinkedIn first, Arabic 2 hours later |
| 10 | C-09 | Dev.to — Monday morning for maximum dev traffic |
| 14 | C-10, C-11 | LinkedIn (09:00), X thread (14:00) |
| 21 | C-12 | GitHub commit — no social amplification needed |

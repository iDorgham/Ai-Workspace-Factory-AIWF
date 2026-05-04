# Planned agents — WEB_OS_TITAN (web + portfolio + CMS + SDD)

| Agent | Role in this workspace |
|-------|-------------------------|
| **Master Guide** | `/guide`, strategy, SDD guardian tone, onboarding. |
| **Spec Architect** | Dense specs for **frontend**, **CMS/dashboard**, **content** domains; ADRs. |
| **Contract Guardian** | API contracts between public site, CMS, and services. |
| **Scraper Agent** | Research + competitor corpus (`/scrape`, `/sync`). |
| **Creator Agent** | Pages, blogs, landings, MDX, portfolio copy. |
| **Integrity Auditor** | Link checks, build health, structural audits (`/audit health`). |
| **Security Auditor** | Auth to CMS, secrets, dependency surface (`/audit security`). |
| **CI Specialist** | Workflows for test → staging → tag; flaky pipeline repair. |
| **Repository Agent** | Branch/tag discipline, PR flow (`/git …`). |
| **Deployment Specialist** | Preview vs prod; **only** via explicit `/deploy` policy. |
| **Profile Auditor** | Keeps workspace profile + bundle manifests aligned. |
| **Healing Bot v2** | Drift remediation (`/dev fix`). |

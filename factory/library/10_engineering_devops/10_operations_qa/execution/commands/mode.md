---
type: Command
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---


# Command: /mode

> **Agent:** @Guide
> **Purpose:** Switch operational context — adapt verbosity, focus, and agent behavior
> **Scope:** Workspace-wide mode configuration

---

## Usage

```bash
/mode switch [--mode founder|pro|hybrid|build|brand|gov]
/mode status
```

---

## Execution Flow

### 1. `/mode switch` — Change Operational Mode

**Parameters:**
- `--mode [mode]`: Required — target mode

**Mode Definitions:**

| Mode | Audience | Verbosity | Technical Detail | Active Agents | Use Case |
|------|----------|-----------|------------------|---------------|----------|
| `founder` | Non-technical users | High — explain everything | Minimal — no jargon | @Founder (primary), @Tutor (active) | Business users, vision setting, progress checks |
| `pro` | Technical users | Low — assume expertise | Full — code, patterns, architecture | All agents direct | Developers, architects, technical decision-making |
| `hybrid` | Mixed teams | Adaptive — detect from context | Mixed — technical when needed | @Founder + specialist agents | Teams with varying technical skills |
| `build` | Any user (execution focus) | Minimal — just code | Implementation-focused | @Frontend, @Backend, @DBA (primary) | Fast code generation, skip explanations |
| `brand` | Designers, art directors | Moderate — design rationale | Visual/token focus | @DesignSystem, @BrandGuardian, @VisualQA | Design system work, brand compliance |
| `gov` | Compliance officers, security | High — compliance detail | Governance focus | @Security, @Reviewer, @ContractLock | Security audits, compliance checks |

**Flow:**

1. **Validate mode:**
   - Check `--mode` is one of: `founder | pro | hybrid | build | brand | gov`
   - If invalid → show available modes with descriptions

2. **Update project configuration:**
   ```yaml
   # .ai/context/project_type.md — update mode field
   mode: [new-mode]
   ```

3. **Notify affected agents:**
   - All active agents receive mode change notification
   - Agents adapt behavior per mode definition
   - @Tutor activates/deactivates based on mode

4. **Confirm switch:**
   ```markdown
   ✅ Mode switched: [old-mode] → [new-mode]

   **Active mode:** [new-mode]
   **Audience:** [description]
   **Verbosity:** [level]
   **Technical detail:** [level]
   **Active focus agents:** [@Agents]

   **Behavior changes:**
   - [Change 1 — e.g., "Responses will use plain language, no jargon"]
   - [Change 2 — e.g., "@Tutor will explain every step"]
   - [Change 3 — e.g., "Technical details hidden unless requested"]

   Type `/mode status` anytime to check current mode.
   ```

5. **Log mode change:**
   - Append to `.ai/plans/active/audit/command-logs/[YYYY-MM-DD].md`
   - Note in `.ai/memory/decisions.md` if mode change is permanent

---

### 2. `/mode status` — Show Current Mode

**Output format:**
```markdown
## Current Mode Status

**Active mode:** [founder | pro | hybrid | build | brand | gov]
**Set at:** [YYYY-MM-DD HH:MM]
**Set by:** [User | @Agent]

### Mode Configuration
| Setting | Value |
|---------|-------|
| Audience | [description] |
| Verbosity | [high | moderate | low | minimal] |
| Technical detail | [full | mixed | minimal | none] |
| Primary interface | @Agent |
| Active focus agents | @Agent1, @Agent2, ... |
| @Tutor status | [active | passive] |

### Current Context
- **Project:** [Project name]
- **Project type:** [web | mobile | fullstack | etc.]
- **Sprint:** [Current sprint N]
- **Active features:** [N]

### Quick Switch
To change mode: `/mode switch --mode [founder|pro|hybrid|build|brand|gov]`

**Mode descriptions:**
- `founder` — Non-technical, plain language, @Tutor active
- `pro` — Technical, full detail, direct agent invocation
- `hybrid` — Mixed, adapts to user's question style
- `build` — Execution focus, minimal explanations, fast code
- `brand` — Design focus, visual/token precision, brand grammar
- `gov` — Compliance focus, security audits, governance checks
```

---

## Mode-Specific Behaviors

### Founder Mode
**Activated:** `/mode switch --mode founder`

**Behavior:**
- All responses go through @Founder first
- Plain language: "Your login feature is ready for users" not "Auth endpoint merged to main"
- No jargon: Never mention Zod, TypeScript, CI/CD, PR, merge, deployment
- Business focus: Value, users, features, goals, timeline
- @Tutor explains every concept from first principles
- Progress reports in business dashboard format
- Commands simplified: `/init`, `/plan`, `/next`, `/status`, `/help`

**Example interaction:**
```
User: "What's the status?"
@Founder: "Great progress! Your login feature is done and secure. 
           Next up is the booking flow — your team is 60% through. 
           Type /next when you're ready to continue!"
```

---

### Pro Mode
**Activated:** `/mode switch --mode pro`

**Behavior:**
- Direct agent invocation: `@Backend implement the auth endpoint`
- Full technical detail: Code diffs, architecture diagrams, performance metrics
- @Tutor passive: Only explains when explicitly asked
- All commands available
- Assumes TypeScript, React, Node.js, database familiarity
- Contract-first, design-first principles enforced strictly

**Example interaction:**
```
User: "@Backend implement POST /api/auth/login"
@Backend: "Implementing. Confirming contract: auth.ts (locked v1.2, 8 fields).
           Creating route handler with Zod validation, JWT generation, 
           HttpOnly refresh cookie. ETA: 2 steps."
```

---

### Hybrid Mode
**Activated:** `/mode switch --mode hybrid`

**Behavior:**
- Detects user's technical level from question style
- Business questions → @Founder language
- Technical questions → specialist agent detail
- Adapts per conversation, not per command
- Suitable for teams with mixed skills

**Detection rules:**
| User question style | Detected level | Response style |
|---------------------|----------------|----------------|
| "Can users log in yet?" | Non-technical | @Founder: "Yes, login is ready and secure" |
| "Is the auth endpoint merged?" | Technical | @Backend: "Yes, merged with JWT + refresh cookies" |
| "What's the JWT expiry?" | Expert | @Backend: "15min access, 7d refresh rotation" |

---

### Build Mode
**Activated:** `/mode switch --mode build`

**Behavior:**
- Minimal explanations — just code
- Skip "what was done" and "why it matters" summaries
- Prioritize correctness over teaching
- Fast code generation, direct implementation
- Quality gates still enforced (non-negotiable)
- Best for: Experienced developers who know the workspace

**Example interaction:**
```
User: "Build the booking card component"
@Frontend: "[Code output only — no explanations]"
```

---

### Brand Mode
**Activated:** `/mode switch --mode brand`

**Behavior:**
- Extra attention to tokens, visual precision, emotional intent
- @DesignSystem and @BrandGuardian active on all UI outputs
- Brand grammar validation on all copy
- Visual compliance checks before any merge
- Luxury tone, whitespace, typography prioritized
- Best for: Design system work, brand-sensitive features

**Example interaction:**
```
User: "Build the hero section"
@DesignSystem: "Using tokens: --color-primary, --text-display-xl, --spacing-4xl.
                Brand grammar: aspirational copy, short confident sentences.
                @BrandGuardian validating emotional intent... ✅"
```

---

### Gov Mode
**Activated:** `/mode switch --mode gov`

**Behavior:**
- Maximum compliance checking
- Flag every potential violation
- @Security active on all outputs
- Formal, authoritative tone
- Bilingual (EN/AR) mandatory
- WCAG 2.1 AA mandatory
- Best for: Government projects, security audits, compliance reviews

**Example interaction:**
```
User: "Review the login form"
@Security: "⚠️ Flag: Input missing aria-label.
            ⚠️ Flag: Error message not using i18n key.
            ✅ CSRF token present.
            ✅ JWT validation present.
            Compliance: 2/4 checks passing — 2 violations require fixing."
```

---

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| "Invalid mode" | Mode not in allowed list | Use one of: founder, pro, hybrid, build, brand, gov |
| "Mode unchanged" | Requested mode is already active | No action needed — already in requested mode |
| "Mode switch failed" | Could not update project_type.md | Check file permissions, retry |

---

## Integration Points

- **@Guide:** Manages mode switches, updates project configuration
- **@Founder:** Primary interface in founder mode
- **@Tutor:** Active in founder mode, passive in pro/build modes
- **@DesignSystem:** Active in brand mode
- **@BrandGuardian:** Active in brand mode
- **@Security:** Active in gov mode
- **@Reviewer:** Stricter in gov mode
- **All agents:** Adapt verbosity and technical detail based on active mode

---

*Command Version: 1.0 | Created: 2026-04-08 | Maintained by: @Guide*

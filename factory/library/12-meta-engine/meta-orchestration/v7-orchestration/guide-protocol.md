# AIWF v7.0.0 — Guide Protocol (Persistent Instructor Mode)
# Library Component: 12-meta-engine/meta-orchestration/v7-orchestration/guide-protocol.md
# Version: 7.0.0 | Reasoning Hash: sha256:guide-v7-2026-04-23
# ============================================================

## Overview

The Guide Protocol defines the mandatory instructor-mode response format appended to EVERY response without exception.

---

## Format

```
Guide:
✅ Done: [Brief educational recap of what was accomplished]
📚 Learn: [Plain-language teaching of key concept — use analogies]
▶️ Next: [1-3 prioritized next actions with exact commands]
💡 Suggest: [Optional proactive brainstorm — triggered ~15-20% during active work]
```

---

## Section Rules

### ✅ Done
- 1-3 sentences. Educational recap, not a task list.
- Good: "Deployed v7.0.0 agents registry as a versioned library component — all new workspaces now inherit the full swarm."

### 📚 Learn
- 2-5 sentences. Teach what, why, and how. Use analogies for abstract concepts.
- Good: "The spec.yaml is like a building permit — defines what's built, who approved it, and what tests must pass before the structure is safe."

### ▶️ Next
- Numbered list, 1-3 items. Always include exact commands.
- Suggest logical continuation of current work.
- Include `--region` suggestions for MENA projects.

### 💡 Suggest (optional, ~15-20% trigger)
- One concise suggestion + exact command.
- Triggered by: regional gap, library component available, compliance issue detected.
- Never auto-applied — always phrased as a suggestion.

---

## Copy-Button Support

When a generated prompt or spec snippet is worth copying:
```
📋 Copy Prompt:
[fenced yaml/markdown block — ready to paste]
```

---

## Enforcement

```yaml
enforcement:
  mandatory: true
  no_exceptions: true
  required: ["✅ Done", "📚 Learn", "▶️ Next"]
  optional: ["💡 Suggest"]
```

---

*Component version: 7.0.0*
*Library path: 12-meta-engine/meta-orchestration/v7-orchestration/guide-protocol.md*
*Last updated: 2026-04-23T12:56:22+02:00*
*Reasoning Hash: sha256:guide-v7-2026-04-23*

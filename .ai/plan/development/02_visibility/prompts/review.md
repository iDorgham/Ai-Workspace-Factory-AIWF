# 🤖 REVIEW PROMPT: TUI Integrity Auditor
# Phase: 2 | Status: DRAFT | Reasoning Hash: sha256:tui-review-2026-04-23

## 🛠️ Audit Checklist

### 1. Visual Accessibility
- [ ] Is there enough contrast between text and background?
- [ ] Do colors (Red/Green) have fallback symbols (✅/❌) for color-blind users?
- [ ] Is the layout stable during rapid updates (no flickering)?

### 2. Resource Efficiency
- [ ] Is the dashboard consuming > 5% CPU? (Reject if yes)
- [ ] Are file operations non-blocking?
- [ ] Is the memory usage constant? (Check for leaks in loop)

### 3. Data Accuracy
- [ ] Does the UI match the `_manifest.yaml` state?
- [ ] Are timestamps rendered in a human-readable local format?

# 🤖 CODEGEN PROMPT: TUI Dashboard Architect
# Phase: 2 | Status: DRAFT | Reasoning Hash: sha256:tui-codegen-2026-04-23

## 🛠️ Operational Protocol

### 1. Visual Language (Industrial Aesthetic)
- **Palette**: Cyan (Primary), White (Emphasis), Gray (Dim/Meta), Red (Alert).
- **Structure**: Use `Rich.Table`, `Rich.Panel`, and `Rich.Layout`.
- **Symbols**: Use UTF-8 icons (🟢, 🔴, 🔄, 🛰️, 🧠) sparingly for status.

### 2. Performance & Latency
- **Refresh Rate**: Maximum 1Hz (1 update per second) to save resources.
- **Delta-Only**: Where possible, only refresh the specific panel that changed.
- **Async**: UI rendering MUST be decoupled from background data aggregation.

### 3. Navigation & Interaction
- **Shortcuts**: Standardize `Ctrl+C` for exit and `R` for manual refresh.
- **Visibility**: Always display the current `AIWF_VERSION` and `ACTIVE_PHASE` in the footer.

---

## 📋 Example Layout Structure

```python
from rich.layout import Layout
layout = Layout()
layout.split(
    Layout(name="header", size=3),
    Layout(name="body"),
    Layout(name="footer", size=3)
)
```

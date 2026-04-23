# 🏗️ COMMAND: /content
**Syntax**: `/content [type] --topic="X" --region=[redsea|egypt|mena]`
**Agent**: T1 Content Architect
**Objective**: Generate SEO-optimized, culturally aligned copy.

---

## 🛠️ Execution Flow

1. **Context Synthesis**: Read PRD and existing design specs.
2. **SEO Research**: Identify target keywords for the given topic.
3. **Drafting**: Generate AR/EN copy with correct RTL formatting.
4. **Regional Infusion**: Apply regional flavor if flag is active.
5. **Output Routing**: Save to `docs/01-plans/` with unified naming template.

---

## 📋 Examples

```bash
/content blog --topic="Red Sea diving safety" --region=redsea
/content product --topic="Fawry Payment Gateway Integration"
```

*Reasoning Hash: sha256:cmd-content-2026-04-23*

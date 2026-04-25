# CLI Prompt: Arabic LinkedIn — C-07-AR-LI

**Task:** Generate Arabic LinkedIn post for MENA audience
**Works with:** Qwen (mandatory — Arabic-first adapter)
**Law 151/2020 flag:** TRUE — run anonymisation before executing this prompt

---

## Pre-Execution Checklist
- [ ] All persona research data anonymised (no names, locations, or identifiers)
- [ ] No Egyptian user data included in prompt payload
- [ ] Anonymisation event logged in tool_performance.jsonl

## Prompt

```
AIWF v21.0.0 Arabic Content Generation

Piece ID: C-07-AR-LI
Channel: LinkedIn (Arabic)
Language: Arabic (full — no transliteration)
Direction: RTL

Write an Arabic LinkedIn post (900 characters max) for the MENA developer audience.

Angle: "Built in Egypt. Compliant with Law 151. Open for the region."

Key messages to convey:
1. AIWF v21 is a sovereign AI workspace factory — governance-first, no data leakage
2. Law 151/2020 (قانون رقم 151 لسنة 2020) is built into every planning phase as an architectural feature
3. Arabic-first content generation is supported via the framework itself

Tone: Warm, founder-to-community. Not sales. Technical but accessible.

Format:
- 3 paragraphs maximum
- Full Arabic script throughout
- 2 hashtags only (Arabic): e.g. #ذكاء_اصطناعي #حوكمة_البيانات
- No English text except technical terms (AIWF, spec, CLI) where no Arabic equivalent exists

Do NOT include:
- Any personal data or user identifiers
- Western-centric framing (e.g. "Silicon Valley approach")
- Transliteration of Arabic words

Reasoning Hash: sha256:aiwf-v21-launch-content-03-C07-arabic-2026-04-25
```

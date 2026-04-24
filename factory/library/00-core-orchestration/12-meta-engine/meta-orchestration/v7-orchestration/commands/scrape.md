# 🏗️ COMMAND: /scrape
**Syntax**: `/scrape [url] --output=[path] --format=[json|markdown]`
**Agent**: T1 Scrape Specialist
**Objective**: Extract structured data from a URL.

---

## 🛠️ Execution Flow

1. **URL Validation**: Verify the target URL is accessible and public.
2. **Scrape Engine Init**: Scrape Specialist identifies the site structure.
3. **Data Harvesting**: Extraction of structured fields.
4. **Law 151/2020 Check**: Audit for PII or sensitive Egyptian data.
5. **Output Routing**: Save result to `docs/01-plans/` or specified path.

---

## 📋 Examples

```bash
/scrape https://example.com/products --format=json
/scrape https://blog.example.com/article --output=research.md
```

*Reasoning Hash: sha256:cmd-scrape-2026-04-23*

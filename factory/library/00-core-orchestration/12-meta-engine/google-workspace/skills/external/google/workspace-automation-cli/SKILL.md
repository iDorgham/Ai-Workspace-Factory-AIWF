# 📊 Google Workspace Automation (CLI)

## Purpose
Enforce standards for programmatic management of Google Workspace assets (Docs, Sheets, Drive). This skill focuses on the CLI-driven automation of reports, document generation, and secure file-sharing orchestration using the Google CLI (`clasp`) and Workspace APIs.

---

## Technique 1 — clasp-driven Deployment (Apps Script)
- **Rule**: Never edit Apps Script in the browser for production projects; use the `clasp` CLI for version control.
- **Protocol**: 
    1. Clone the Apps Script project locally.
    2. Use TypeScript for all script logic.
    3. Deploy versions to specific "environments" (e.g., prod vs dev).

---

## Technique 2 — Programmatic Report Generation (Sheets)
- **Rule**: Use the "Template & Populate" pattern to ensure consistent formatting.
- **Protocol**: 
    1. Define a Master Sheet with specific styles and data validation.
    2. Copy the template via Drive API.
    3. Inject data into specific A1 notation ranges using the Sheets API.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Broad OAuth Scopes** | Security risk | Use the "Least Privilege" principle; only request `drive.file` instead of `drive.readonly` if possible. |
| **Hard-coded File IDs** | Broken workflows | Use naming conventions or metadata tags to discover files dynamically instead of static IDs. |
| **Ignoring Batch Update Limits** | Performance throttling | Use `batchUpdate` for multiple Sheet edits to stay within API rate limits. |

---

## Success Criteria (Workspace QA)
- [ ] Apps Script code is 100% version-controlled via Git.
- [ ] 0 Broad Scopes used in Service Accounts.
- [ ] Automated reports are generated and shared within < 5s.
- [ ] Sheets data is validated before injection to prevent formula corruption.
- [ ] Arabic RTL alignment is correctly set for all generated MENA reports.
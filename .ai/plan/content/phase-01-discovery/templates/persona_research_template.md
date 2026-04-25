# Persona Research Template

**Use when:** Defining or updating audience personas for any content plan.

---

## Persona Definition Block

```markdown
## Persona: {{PERSONA_NAME}}

**Role:** {{JOB_TITLE}}
**Age Range:** {{RANGE}}
**Region:** {{PRIMARY_REGION}}
**Signal Source:** {{WHERE_DID_THIS_COME_FROM — e.g., "AIWF workflow.jsonl client patterns", "community observation"}}

### Pain Points
1. {{PAIN_1}}
2. {{PAIN_2}}
3. {{PAIN_3}}

### AIWF Use Case
{{HOW_THIS_PERSON_USES_OR_WOULD_USE_AIWF}}

### Content Preferences
- **Format:** {{blog|thread|video|architecture_diagram|case_study}}
- **Depth:** {{beginner|intermediate|advanced|executive}}
- **Language:** {{English|Arabic|Bilingual}}
- **Channel:** {{GitHub|LinkedIn|X|Community}}

### Message That Resonates
"{{ONE_SENTENCE_THAT_MAKES_THIS_PERSONA_STOP_SCROLLING}}"

### Law 151 Note
{{IS_THIS_PERSONA_EGYPTIAN — yes/no. If yes: all demographic signals anonymised.}}
```

---

## CLI Prompt for Persona Generation

Paste into any CLI after loading system_prompt.md:

```
Generate a detailed audience persona for AIWF v21.0.0 content strategy.

Role: {{ROLE}}
Region: {{REGION}}
Context: AIWF is a sovereign AI orchestration factory built in Egypt with Law 151/2020
compliance, multi-LLM orchestration, and the Tripartite Planning Singularity (v21.0.0).

Output:
- Pain points (3)
- AIWF use case (1 paragraph)
- Preferred content format and channel
- The single message that makes them stop scrolling
- Law 151 data handling note if Egyptian

Reasoning Hash: sha256:persona-{{ROLE_SLUG}}-2026-04-25
```

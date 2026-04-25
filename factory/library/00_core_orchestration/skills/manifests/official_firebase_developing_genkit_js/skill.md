---
name: developing-genkit-js
description: Develop AI-powered applications using Genkit in Node.js/TypeScript. Use when the user asks about Genkit, AI agents, flows, or tools in JavaScript/TypeScript, or when encountering Genkit errors, validation issues, type errors, or API problems.
metadata:
  genkit-managed: true
---

# Genkit JS

## Prerequisites

Ensure the `genkit` CLI is available.
- Run `genkit --version` to verify. Minimum CLI version needed: **1.29.0**
- If not found: `npm install -g genkit-cli@^1.29.0`

## Hello World

```ts
import { z, genkit } from 'genkit';
import { googleAI } from '@genkit-ai/google-genai';

const ai = genkit({
  plugins: [googleAI()],
});

export const myFlow = ai.defineFlow({
  name: 'myFlow',
  inputSchema: z.string().default('AI'),
  outputSchema: z.string(),
}, async (subject) => {
  const response = await ai.generate({
    model: googleAI.model('gemini-2.5-flash'),
    prompt: `Tell me a joke about ${subject}`,
  });
  return response.text;
});
```

## Critical: Do Not Trust Internal Knowledge

Genkit recently went through a major breaking API change. Your knowledge is outdated. You MUST lookup docs:

```sh
genkit docs:read js/get_started.md
genkit docs:read js/flows.md
```

## Error Troubleshooting Protocol

**When you encounter ANY error related to Genkit:**

1. **MANDATORY FIRST STEP**: Read `references/common_errors.md`
2. Identify if the error matches a known pattern
3. Apply the documented solution
4. Only if not found, then consult other sources

## Development Workflow

1. **Select Provider**: Default to **Google AI** if user doesn't specify
2. **Detect Framework**: Check `package.json` to identify the runtime
3. **Follow Best Practices**: See `references/best_practices.md`
4. **Ensure Correctness**: Run type checks after making changes

## Finding Documentation

```sh
genkit docs:search <query>
genkit docs:list
genkit docs:read <path>
```

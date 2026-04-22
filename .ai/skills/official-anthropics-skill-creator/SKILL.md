---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

## Process Overview

1. Decide what you want the skill to do and roughly how it should do it
2. Write a draft of the skill
3. Create a few test prompts and run claude-with-access-to-the-skill on them
4. Help the user evaluate the results both qualitatively and quantitatively
5. Rewrite the skill based on feedback
6. Repeat until satisfied
7. Expand the test set and try again at larger scale

## Creating a skill

### Capture Intent

Start by understanding the user's intent:

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works?

### Skill Structure

A good skill has:
- A clear `name` and `description` in the frontmatter
- Specific trigger conditions
- Step-by-step instructions
- Examples of good outputs
- Edge cases and how to handle them

### Communicating with the user

Pay attention to context cues to understand how to phrase your communication. Explain technical terms if you're in doubt about the user's familiarity.

## Optimizing Skill Descriptions

After the skill is done, run the skill description improver to optimize triggering accuracy. The description is what determines when the skill gets activated, so it needs to be precise and comprehensive.

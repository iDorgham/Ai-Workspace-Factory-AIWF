# Templates

Human-editable content blueprints and schemas used by `/brand`, `/create`, and export flows. Agents read from here; they do not overwrite these files (see `.ai/data-ownership*.md`).

## Design Catalog

Imported design references are available under `design/[provider]/design.md`, sourced from:
- `https://github.com/VoltAgent/awesome-design-md/tree/main/design-md`

Use `/design list` to browse and `/design use [provider]` to select.

## Claude Subagents Catalog

Imported Claude subagents are available under `subagents/claude/categories/`, sourced from:
- `https://github.com/VoltAgent/awesome-claude-code-subagents/tree/main/categories`

Use `subagents/claude/catalog.json` for machine-readable category/subagent descriptions.

## Codex Subagents Catalog

Imported Codex subagents catalog is available under `subagents/codex/categories/`, sourced from:
- `https://github.com/VoltAgent/awesome-codex-subagents/tree/main/categories`

Use `subagents/codex/catalog.json` for machine-readable category summaries.

## Content Template Contract

All content templates in this workspace should follow this normalized contract:

- Include a frontmatter block with: `title`, `meta_description`, `keywords`, `slug`, `content_type`, `author`, `created_at`, `version`, and `status`.
- Use explicit `[PLACEHOLDER]` tokens for required user/context values.
- Include section-level purpose and expected length so generation stays consistent.
- Include an SEO checklist that aligns with `/review` gates.
- Target a deterministic output path under `content/sovereign/*`.

Canonical command-routing reference for command docs: `.ai/registry/routing/command_routing.json`.

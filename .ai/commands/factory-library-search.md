# `/factory library search [type] [tag]`

## Syntax
`/factory library search [type] [tag]`

## Required Inputs
- Client/profile arguments as specified in syntax.

## Outputs
- Terminal status summary.
- Updated files under `factory/intake`, `factory/manifests`, `workspaces/<slug>`, or `factory/reports` depending on command.

## Failure Conditions
- Missing source path, missing profile, invalid intake data, dependency mismatch, or validation failure.

## Beginner Example
`/factory library search skills seo`

## Purpose
Search indexed library items by component type and tag.

# `/factory intake [client]`

## Syntax
`/factory intake [client]`

## Required Inputs
- Client/profile arguments as specified in syntax.

## Outputs
- Terminal status summary.
- Updated files under `factory/intake`, `factory/manifests`, `workspaces/<slug>`, or `factory/reports` depending on command.

## Failure Conditions
- Missing source path, missing profile, invalid intake data, dependency mismatch, or validation failure.

## Beginner Example
`/factory intake acme`

## Purpose
Run guided intake and persist client intake JSON.

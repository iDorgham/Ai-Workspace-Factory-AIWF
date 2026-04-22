# `/factory compose [client] [--profile]`

## Syntax
`/factory compose [client] [--profile]`

## Required Inputs
- Client/profile arguments as specified in syntax.

## Outputs
- Terminal status summary.
- Updated files under `factory/intake`, `factory/manifests`, `workspaces/<slug>`, or `factory/reports` depending on command.

## Failure Conditions
- Missing source path, missing profile, invalid intake data, dependency mismatch, or validation failure.

## Beginner Example
`/factory compose acme --profile fullstack-saas`

## Purpose
Compose workspace component set and produce composition manifest.

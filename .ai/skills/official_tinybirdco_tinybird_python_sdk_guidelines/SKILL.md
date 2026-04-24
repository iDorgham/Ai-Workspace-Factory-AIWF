---
name: tinybird-python-sdk-guidelines
description: Tinybird Python SDK for defining datasources, pipes, and queries in Python. Use when working with tinybird-sdk, Python Tinybird projects, or data ingestion and queries in Python.
---

# Tinybird Python SDK Guidelines

Guidance for using the `tinybird-sdk` package to define Tinybird resources in Python.

## When to Apply

- Installing or configuring tinybird-sdk
- Defining datasources, pipes, or endpoints in Python
- Creating Tinybird clients in Python
- Using data ingestion or queries in Python
- Running tinybird dev/build/deploy commands for Python projects
- Migrating from legacy .datasource/.pipe files to Python
- Defining connections (Kafka, S3, GCS)
- Creating materialized views, copy pipes, or sink pipes

## Rule Files

- `rules/getting_started.md`
- `rules/configuration.md`
- `rules/defining_datasources.md`
- `rules/defining_endpoints.md`
- `rules/client.md`
- `rules/low_level_api.md`
- `rules/cli_commands.md`
- `rules/connections.md`
- `rules/materialized_views.md`
- `rules/copy_sink_pipes.md`
- `rules/tokens.md`

## Quick Reference

- Install: `pip install tinybird-sdk`
- Initialize: `tinybird init`
- Dev mode: `tinybird dev` (uses configured `dev_mode`, typically branch)
- Build: `tinybird build` (builds against configured dev target)
- Deploy: `tinybird deploy` (deploys to main/production)
- Preview in CI: `tinybird preview`
- Migrate: `tinybird migrate` (convert .datasource/.pipe files to Python)
- Server-side only; never expose tokens in browsers

---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---

# Docker MCP Protocol (Sovereign CLI Bridge)

## Purpose

This skill defines the industrial protocols for managing Docker environments within the AI Workspace Factory. Since the environment uses the Docker CLI directly, this skill maps standard MCP actions to sovereign `docker` commands.

## Task → Command Mapping

| Task | Command | Industrial Protocol |
|------|---------|---------------------|
| List Environments | `docker ps -a` | Must include `--format` for machine-readable parsing. |
| Inspect Container | `docker inspect <id>` | Always check for Law 151/2020 compliance labels. |
| Run Test Shard | `docker run --rm ...` | Use isolated networks; never expose sensitive ports. |
| Build Image | `docker build -t ...` | Silent versioning; tag with `v{major}.{minor}.{patch}`. |
| Execute Audit | `docker exec <id> ...` | Log all internal mutations to `.ai/logs/`. |

## 🌍 Regional Calibration (MENA Context)

- **Data Sovereignty:** All containers handling MENA sensitive data MUST be labeled with `residency=mena-soil`.
- **Compliance:** Verify that images are pulled from approved registries (e.g. sovereign mirror).

## 🛡️ Critical Failure Modes (Anti-Patterns)

- **Anti-Pattern:** Running as root -> *Correction:* Use non-root users in Dockerfiles.
- **Anti-Pattern:** Persistent residue -> *Correction:* Use `--rm` or `docker system prune` regularly.

## 📋 Industrial Standard

All Docker interactions must be recorded in the append-only audit trail.
Reasoning Hash: `{{REASONING_HASH}}`
Timestamp: `{{ISO8601}}`

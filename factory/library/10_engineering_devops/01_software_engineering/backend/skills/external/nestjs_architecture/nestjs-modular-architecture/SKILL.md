---
type: Skill
subagents: [core-validator, integrity-bot]
agents: [master-guide, swarm-router]
dependencies: [core-orchestration, global-sync]
version: 1.0.0
---



# 🦅 NestJS Modular Architecture

## Purpose
Enforce standards for high-performance, maintainable Node.js backends using NestJS. This skill focuses on Dependency Injection (DI), Module isolation, and the implementation of Clean Architecture principles (Controllers, Services, Repositories).

---

## Technique 1 — Domain-Driven Module Isolation
- **Rule**: Organize the application into self-contained "Feature Modules" (e.g., `UsersModule`, `AuthModule`) that own their logic, controllers, and providers.
- **Protocol**: 
    1. Define a `*.module.ts` for each core domain.
    2. Explicitly `export` only the services required by other modules.
    3. Use `ForwardRef` sparingly; prioritize interface-based abstraction for tight coupling.

---

## Technique 2 — Global Interceptors & Exception Filters
- **Rule**: Centralize "Cross-Cutting Concerns" (Logging, Error Formatting, Data Transformation) using NestJS Interceptors and Filters.
- **Protocol**: 
    1. Implement a `GlobalExceptionFilter` to ensure all API errors follow a standardized JSON format.
    2. Use `TransformInterceptors` to strip internal sensitive fields from response objects automatically.
    3. Implement `ValidationPipes` with `class-validator` for automated DTO (Data Transfer Object) validation.

---

## 🛡️ Critical Failure Modes (Anti-Patterns)

| Anti-Pattern | Result | Correction |
| :--- | :--- | :--- |
| **Logic in Controllers** | Testing difficulty / Bloat | Controllers must ONLY handle routing and request/response orchestration; move all business logic to Services. |
| **Monolithic Shared Module** | Dependency loop chaos | Break down the shared module into atomic "Utility Modules" based on specific functionality (e.g., `ConfigModule`, `LoggerModule`). |
| **Ignoring Database Transactions** | Data inconsistency | Use Transactional interceptors or decorators to ensure multi-step DB updates are atomic. |

---

## Success Criteria (NestJS QA)
- [ ] 100% of API endpoints follow the defined DTO structure.
- [ ] Dependency injection is used for 100% of external integrations (DB, API, Mail).
- [ ] Modular boundaries are strictly enforced (no cross-module folder imports).
- [ ] 80%+ Unit and Integration test coverage for Services and Controllers.
# Authly

Authly is a fictional developer authentication and authorization platform used as a living test environment for Draftly.

The initial implementation intentionally stays small. It provides an in-memory Python SDK for:

- users
- password authentication
- sessions
- organizations
- roles and permissions
- OAuth authorization URLs
- token creation
- signed webhooks

The repository is designed to evolve through simulated releases and documentation-drift scenarios. Future product changes should intentionally create documentation problems that Draftly can detect, evaluate, and remediate.

> **Important:** Authly is a fictional benchmark application. The authentication primitives in this repository are intentionally simplified and are not suitable for production identity/security workloads.

## Quick start

```bash
uv sync
uv run pytest
uv run python examples/basic_login.py
```

Or install the package in editable mode:

```bash
pip install -e .
```

## Initial product scope

Version `0.1.0` intentionally focuses on a small surface:

```text
User
  ↓
Password authentication
  ↓
Session
  ↓
Organization
  ↓
Role
  ↓
Permission
```

OAuth URL construction, token creation, and webhook signing are included as small primitives so later simulation scenarios have realistic code surfaces to evolve.

## Draftly benchmark role

Authly is not intended to be a complete SaaS product. Its purpose is to behave like a small startup repository that changes over time.

Examples of planned changes:

- OAuth and PKCE
- API-key deprecation
- RBAC expansion
- refresh-token rotation
- SDK breaking changes
- security configuration changes
- migration requirements

See `simulation/roadmap.md` and `simulation/scenarios/`.

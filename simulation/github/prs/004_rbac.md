# PR #125 — Expand RBAC

**Status:** merged  
**Author:** @jordan  
**Labels:** feature, authorization  
**Milestone:** v0.5.0

## Title

feat: add organization-scoped RBAC

## Description

Expands Authly authorization with organization-scoped roles.

### Changes

- Add organization-scoped roles.
- Add custom roles.
- Add permission inheritance.
- Allow users to have different roles in different organizations.

## Documentation impact

Affected:

- `docs/authorization.md`
- `docs/organizations.md`
- `docs/roles.md`
- `docs/permissions.md`
- `examples/organizations.py`
- `examples/role_based_access.py`

## Review comments

### @maya

The current documentation implies roles are globally assigned to users.

That will no longer be correct.

### @jordan

Good catch. The role documentation needs to explain organization scope.

## Merge

Merged into `main`.

Release target: `v0.5.0`

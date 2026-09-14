# API reference

Complete reference for the Authly SDK: installation, client construction, every service method, the returned data models, the error catalog, and the CLI.

## SDK overview

Authly ships as a single Python package, `authly`, requiring Python 3.11 or newer. It is an in-memory SDK: all state lives on the client instance and disappears when the process exits. The client is deliberately not an HTTP client; there is no network I/O.

### Installation

```bash
pip install -e .
```

or, from the repository root:

```bash
uv sync
```

The installed version is available as `authly.__version__` (`0.1.0`).

## Client constructor

`Authly(*, project_id: str, api_key: str)`

Creates the client and all service namespaces. Raises `ValueError` if either argument is empty.

```python
from authly import Authly

authly = Authly(
    project_id="proj_demo",
    api_key="demo_key",
)
```

| Parameter    | Type | Required | Notes                                        |
| ------------ | ---- | -------- | -------------------------------------------- |
| `project_id` | str  | yes      | Empty value raises `ValueError`.             |
| `api_key`    | str  | yes      | Empty value raises `ValueError`.             |

Both parameters are keyword-only.

## Service namespaces

Every service is instantiated by the client and reachable as an attribute:

| Attribute            | Service              | Purpose                                  |
| -------------------- | -------------------- | ---------------------------------------- |
| `authly.users`       | `UserService`        | Create and look up users                 |
| `authly.auth`        | `AuthService`        | Password login                           |
| `authly.sessions`    | `SessionService`     | Create, get, revoke sessions             |
| `authly.organizations` | `OrganizationService` | Organizations and membership          |
| `authly.roles`       | `RoleService`        | Roles, permissions, assignments          |
| `authly.permissions` | `PermissionService`  | Permission checks                        |
| `authly.oauth`       | `OAuthClient`        | Authorization URL construction           |
| `authly.tokens`      | `TokenService`       | Token primitives                         |
| `authly.webhooks`    | `WebhookService`     | HMAC signing and verification            |

## Top-level exports

```python
from authly import (
    Authly,
    AuthlyError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    OAuthClient,
    Token,
)
```

`AuthlyError` and its subclasses are described in [Troubleshoot errors](../how-to/troubleshooting.md).

## UserService

`authly.users`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `create` | `(*, email: str, name: str, password: str)` | `User` | `ValidationError` if email is empty or lacks `@`, or password is empty |
| `get` | `(user_id: str)` | `User` | `NotFoundError` for unknown ID |
| `list` | `()` | `list[User]` | — |

Duplicate emails are permitted; only the first matching user is found at login.

## AuthService

`authly.auth`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `login` | `(*, email: str, password: str)` | `Session` | `AuthenticationError` when email/password do not match |

A successful login also stores a new session via `SessionService`.

## SessionService

`authly.sessions`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `create` | `(*, user_id: str)` | `Session` | — |
| `get` | `(session_id: str)` | `Session` | `NotFoundError` for unknown ID |
| `revoke` | `(session_id: str)` | `Session` | `NotFoundError` for unknown ID |

`revoke()` sets `active = False`. There is no `list()`.

## OrganizationService

`authly.organizations`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `create` | `(*, name: str)` | `Organization` | — |
| `add_member` | `(*, organization_id: str, user_id: str)` | `Organization` | `NotFoundError` for unknown organization ID |
| `get` | `(organization_id: str)` | `Organization` | `NotFoundError` for unknown ID |

`add_member()` does not verify that the user exists.

## RoleService

`authly.roles`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `create` | `(*, name: str, permissions: set[str] \| None = None)` | `Role` | — |
| `assign` | `(*, user_id: str, role_id: str)` | `Role` | `NotFoundError` for unknown role ID |
| `get` | `(role_id: str)` | `Role` | `NotFoundError` for unknown ID |

`assign()` adds the user ID to the role's `assignments` set.

## PermissionService { #permissionservice }

`authly.permissions`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `check` | `(*, user_id: str, permission: str)` | `bool` | `AuthorizationError` when no assigned role contains the permission |
| `list_for_user` | `(*, user_id: str)` | `set[str]` | — |

`check()` returns `True` or raises; it never returns `False`. Unknown users raise because they hold no roles. `list_for_user()` never raises and returns an empty set for unknown users.

## OAuthClient { #oauthclient }

`authly.oauth`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `authorization_url` | `(*, provider: str, redirect_uri: str, state: str)` | `str` | — |

Builds `https://auth.example.test/oauth/authorize?...` with `client_id` set to `project_id` and `response_type=code`. No token exchange or PKCE in 0.1.

## TokenService

`authly.tokens`

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `create` | `(*, user_id: str, expires_in_seconds: int = 3600)` | `Token` | — |
| `is_expired` | `(token: Token)` | `bool` | — |

Expiry compares `expires_at` against the current UTC time.

## WebhookService { #webhookservice }

`authly.webhooks` — both methods are static and callable on the class.

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `sign` | `(*, payload: dict, secret: str)` | `str` | — |
| `verify` | `(*, payload: dict, signature: str, secret: str)` | `bool` | — |

HMAC-SHA256 over canonical JSON (sorted keys, compact separators). `verify()` uses a constant-time comparison.

## Data models

Services return dataclass instances. All use `slots=True`, expose plain attributes, and carry generated IDs with type-specific prefixes.

### ID prefixes

| Prefix  | Resource      | Format                |
| ------- | ------------- | --------------------- |
| `usr_`  | User          | prefix + 10 hex chars |
| `sess_` | Session       | prefix + 10 hex chars |
| `org_`  | Organization  | prefix + 10 hex chars |
| `role_` | Role          | prefix + 10 hex chars |
| `tok_`  | Token         | prefix + 10 hex chars |

### User

Returned by `users.create()`, `users.get()`, `users.list()`.

| Field       | Type | Notes                                    |
| ----------- | ---- | ---------------------------------------- |
| `id`        | str  | `usr_...`                                |
| `email`     | str  | Validated at creation; may be duplicated across users |
| `name`      | str  | Display name                             |
| `password`  | str  | Stored as provided — benchmark simplification, see [Concepts](../explanation/concepts.md) |

### Session { #session }

Returned by `auth.login()`, `sessions.create()`, `sessions.get()`, `sessions.revoke()`.

| Field        | Type       | Notes                          |
| ------------ | ---------- | ------------------------------ |
| `id`         | str        | `sess_...`                     |
| `user_id`    | str        | Owning user                    |
| `created_at` | datetime   | UTC timestamp                  |
| `active`     | bool       | Defaults to `True`; `revoke()` sets it to `False` |

### Organization { #organization }

Returned by `organizations.create()`, `organizations.add_member()`, `organizations.get()`.

| Field         | Type      | Notes                                     |
| ------------- | --------- | ----------------------------------------- |
| `id`          | str       | `org_...`                                 |
| `name`        | str       | Organization name                         |
| `member_ids`  | set[str]  | User IDs; mutated in place by `add_member()` |

### Role { #role }

Returned by `roles.create()`, `roles.assign()`, `roles.get()`.

| Field          | Type      | Notes                                        |
| -------------- | --------- | -------------------------------------------- |
| `id`           | str       | `role_...`                                   |
| `name`         | str       | Role name; not used for lookups              |
| `permissions`  | set[str]  | Permission strings such as `documents:write` |
| `assignments`  | set[str]  | User IDs the role is assigned to             |

Because `permissions` and `assignments` are sets, duplicate inserts are no-ops and membership tests are O(1).

### Token

Returned by `tokens.create()`; accepted by `tokens.is_expired()`.

| Field         | Type       | Notes                                  |
| ------------- | ---------- | -------------------------------------- |
| `id`          | str        | `tok_...`                              |
| `user_id`     | str        | Owning user                            |
| `value`       | str        | URL-safe random token string           |
| `expires_at`  | datetime   | UTC; creation time plus `expires_in_seconds` |
| `token_type`  | str        | Always `"access"`                      |

`Token` is exported at the package root (`from authly import Token`); the other models are not.

## CLI

Installing the package registers an `authly` console script (see `[project.scripts]` in `pyproject.toml`). The CLI is intentionally minimal in version 0.1 and performs no network or state operations.

### `authly login`

Authenticate a local project session:

```bash
authly login --project proj_demo
```

Output:

```text
Authenticated local CLI session for proj_demo
```

`--project` is required; omitting it prints an argparse error and exits with status 2.

### `authly user list`

```bash
authly user list
```

Output:

```text
The benchmark CLI does not connect to a remote API yet.
```

The command always prints this placeholder regardless of arguments.

### No command

Running `authly` with no subcommand prints the help text:

```text
usage: authly [-h] {login,user} ...
```

### Exit codes

The CLI uses argparse defaults: `0` on success, `2` on usage errors. It never reads or mutates SDK state.
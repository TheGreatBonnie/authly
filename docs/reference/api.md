# API reference

## Authly client

The `Authly` class is the entry point for the SDK.

### Constructor

```python
Authly(project_id: str, api_key: str)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `project_id` | `str` | Your Authly project identifier |
| `api_key` | `str` | API key for authentication |

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `users` | `UserService` | User management |
| `sessions` | `SessionService` | Session management |
| `oauth` | `OAuthClient` | OAuth authorization URL and code exchange |
| `tokens` | `TokenService` | Token creation and validation |
| `organizations` | `OrganizationService` | Organization management |
| `roles` | `RoleService` | Role management |
| `permissions` | `PermissionService` | Permission checks |
| `webhooks` | `WebhookService` | Webhook signature verification |

## UserService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `create` | `(*, email: str, name: str, password: str)` | `User` | `ValidationError` when fields are empty |
| `get` | `(user_id: str)` | `User` | `NotFoundError` when user does not exist |
| `list` | `()` | `list[User]` | — |

## SessionService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `create` | `(*, user_id: str)` | `Session` | `NotFoundError` when user does not exist |
| `get` | `(session_id: str)` | `Session` | `NotFoundError` when session does not exist |
| `revoke` | `(session_id: str)` | `None` | `NotFoundError` when session does not exist |

## AuthService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `login` | `(*, email: str, password: str)` | `Token` | `AuthenticationError` when credentials are invalid |

A successful login also stores a new session via `SessionService`.

## OAuthClient

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `authorization_url` | `(*, provider: str, redirect_uri: str, state: str)` | `str` | — |
| `exchange_code` | `(*, provider: str, code: str, redirect_uri: str)` | `Token` | `ValidationError` when `provider`, `code`, or `redirect_uri` is empty |

`authorization_url` builds `https://auth.example.test/oauth/authorize?...` with `client_id` set to `project_id` and `response_type=code`.

`exchange_code` exchanges an OAuth authorization code for an access token. It creates a deterministic identity user per `provider`/`code` pair and returns a new access token. The implementation:

- Computes a SHA256 digest of the authorization code (first 12 characters) — the raw code is never stored
- Creates an identity email in the format `{provider}:{digest}@oauth.example.test`
- Reuses existing users with matching emails or creates new ones with a random password
- Returns a fresh `Token` for the identity user

PKCE is not implemented in 0.1.

## TokenService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `create` | `(*, user_id: str)` | `Token` | `NotFoundError` when user does not exist |
| `validate` | `(token: str)` | `Token` | `AuthenticationError` when token is invalid or expired |

## OrganizationService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `create` | `(*, name: str)` | `Organization` | `ValidationError` when name is empty |
| `get` | `(org_id: str)` | `Organization` | `NotFoundError` when organization does not exist |
| `add_member` | `(org_id: str, user_id: str)` | `None` | `NotFoundError` when organization or user does not exist |

## RoleService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `create` | `(*, name: str, permissions: list[str])` | `Role` | `ValidationError` when name is empty |
| `get` | `(role_id: str)` | `Role` | `NotFoundError` when role does not exist |
| `assign` | `(user_id: str, role_id: str)` | `None` | `NotFoundError` when user or role does not exist |

## PermissionService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `check` | `(*, user_id: str, permission: str)` | `bool` | `NotFoundError` when user does not exist |

## WebhookService

### Methods

| Method | Signature | Returns | Raises |
|--------|-----------|---------|--------|
| `sign` | `(*, payload: bytes, secret: str)` | `str` | — |
| `verify` | `(*, payload: bytes, signature: str, secret: str)` | `bool` | — |

## Data models

### User

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier |
| `email` | `str` | Email address |
| `name` | `str` | Display name |
| `password` | `str` | Password (stored unhashed) |

### Session

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier |
| `user_id` | `str` | Associated user ID |
| `created_at` | `datetime` | Creation timestamp |
| `expires_at` | `datetime` | Expiration timestamp |

### Token

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | `str` | The token string |
| `token_type` | `str` | Always `"access"` |
| `user_id` | `str` | Associated user ID |
| `expires_at` | `datetime` | Expiration timestamp |

### Organization

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier |
| `name` | `str` | Organization name |
| `members` | `list[str]` | List of user IDs |

### Role

| Field | Type | Description |
|-------|------|-------------|
| `id` | `str` | Unique identifier |
| `name` | `str` | Role name |
| `permissions` | `list[str]` | List of permission strings |

## Exceptions

| Exception | Description |
|-----------|-------------|
| `ValidationError` | Raised when input validation fails |
| `AuthenticationError` | Raised when authentication fails |
| `NotFoundError` | Raised when a requested resource does not exist |

## References

- `docs/reference/api.md`
- `docs/how-to/oauth-authorization-url.md`
- `src/authly/oauth.py`
- `https://github.com/TheGreatBonnie/authly/pull/43`
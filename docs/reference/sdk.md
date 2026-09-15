# SDK reference

## Installation

```bash
pip install authly
```

## Quick start

```python
from authly import Authly

authly = Authly(project_id="proj_123", api_key="key_456")

# Create a user
user = authly.users.create(
    email="alice@example.com",
    name="Alice",
    password="secret123",
)

# Log in
token = authly.auth.login(
    email="alice@example.com",
    password="secret123",
)

print(token.access_token)
```

## Services

Every service is instantiated by the client and reachable as an attribute:

| Attribute | Service | Purpose |
|-----------|---------|---------|
| `authly.users` | `UserService` | Create and manage users |
| `authly.sessions` | `SessionService` | Session lifecycle |
| `authly.auth` | `AuthService` | Login and token issuance |
| `authly.organizations` | `OrganizationService` | Organizations and membership |
| `authly.roles` | `RoleService` | Roles, permissions, assignments |
| `authly.permissions` | `PermissionService` | Permission checks |
| `authly.oauth` | `OAuthClient` | Authorization URL and code exchange |
| `authly.tokens` | `TokenService` | Token primitives |
| `authly.webhooks` | `WebhookService` | HMAC signing and verification |

## OAuth

The `OAuthClient` provides OAuth 2.0 authorization code flow support:

### Build authorization URL

```python
url = authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://example.com/callback",
    state="random-state",
)
```

### Exchange authorization code

```python
token = authly.oauth.exchange_code(
    provider="github",
    code="code-from-callback",
    redirect_uri="https://example.com/callback",
)
```

See [Construct an OAuth authorization URL](../how-to/oauth-authorization-url.md) for details on the deterministic identity creation process.

## References

- `docs/reference/sdk.md`
- `docs/how-to/oauth-authorization-url.md`
- `docs/reference/api.md`
- `https://github.com/TheGreatBonnie/authly/pull/43`
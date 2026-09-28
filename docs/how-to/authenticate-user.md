# Authenticate a user

Use this recipe to log a user in with email and password or via OAuth and obtain a session.

## Prerequisites

- An initialized client ([Configure the client](configure-client.md))
- A user created with `authly.users.create()`

## Log in with email and password

```python
session = authly.auth.login(
    email="alice@example.com",
    password="secret",
)

print(session.id)      # sess_7d21e5a09c
print(session.user_id) # usr_4f8a2c1b9d
print(session.active)  # True
```

A successful login creates a new session owned by the matching user.

## Log in with OAuth

Use `login_with_oauth()` to authenticate a user via an OAuth provider. This method exchanges an authorization code for an access token and creates a session.

```python
session = authly.auth.login_with_oauth(
    provider="google",
    code="4/0AX4XfW...",
    redirect_uri="https://example.com/callback",
)

print(session.id)      # sess_9a8b7c6d5e
print(session.user_id) # usr_1f2e3d4c5b
print(session.active)  # True
```

### OAuth parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | `str` | Yes | OAuth provider name (e.g., `"google"`, `"github"`) |
| `code` | `str` | Yes | Authorization code returned by the provider |
| `redirect_uri` | `str` | Yes | Must match the redirect URI registered with the provider |

The method validates the authorization code with the provider, retrieves the user's profile information, and creates a new session. If the user does not exist, a new user record is created automatically.

## Handle failed logins

An unknown email or a wrong password raises `AuthenticationError` with the message `invalid email or password`. The error does not reveal which of the two was wrong:

```python
from authly import AuthenticationError

try:
    authly.auth.login(email="alice@example.com", password="oops")
except AuthenticationError as exc:
    print(f"login failed: {exc}")
```

OAuth logins may raise `AuthenticationError` if the authorization code is invalid, expired, or the redirect URI does not match.

## Email lookup behavior

`login()` matches against the first user registered with that email address. Creating two users with the same email is allowed, but only the first one can ever match a login. Avoid duplicate emails.

## Revoke the session later

Revoking sets `active` to `False`; see [Create and revoke sessions](manage-sessions.md).

## See also

- [Sessions data model](../reference/data-models.md)
- [Troubleshoot errors](troubleshoot-errors.md)

## References

- docs/how-to/authenticate-user.md
- src/authly/auth.py
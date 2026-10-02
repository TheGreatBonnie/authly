# API Reference

Complete reference for the Authly API.

## TokenService

`authly.tokens`

The TokenService provides methods for creating, validating, and revoking authentication tokens.

| Method | Signature | Returns | Raises |
| ------ | --------- | ------- | ------ |
| `create` | `(*, user_id: str, expires_in_seconds: int = 3600)` | `Token` | — |
| `is_expired` | `(token: Token)` | `bool` | — |
| `revoke` | `(token: str)` | `None` | — |

### create

Creates a new authentication token for the specified user.

**Parameters:**

- `user_id` (str, required): The unique identifier of the user.
- `expires_in_seconds` (int, optional): Token lifetime in seconds. Defaults to `3600` (1 hour).

**Returns:**

A `Token` object containing:
- `token`: The token string
- `user_id`: The associated user ID
- `expires_at`: UTC expiration timestamp

**Example:**

```python
from authly.tokens import create

token = create(user_id="user_123", expires_in_seconds=3600)
```

### is_expired

Checks whether a token has expired by comparing `expires_at` against the current UTC time.

**Parameters:**

- `token` (Token, required): The token to check.

**Returns:**

- `bool`: `True` if the token has expired, `False` otherwise.

**Example:**

```python
from authly.tokens import create, is_expired

token = create(user_id="user_123")
if is_expired(token):
    print("Token has expired")
```

### revoke

Revokes an authentication token, removing it from the client. This method is idempotent and never raises an error, even if the token does not exist.

**Parameters:**

- `token` (str, required): The token string to revoke.

**Returns:**

- `None`

**Example:**

```python
from authly.tokens import revoke

revoke("token_string_here")
```

## References

- docs/reference/api.md
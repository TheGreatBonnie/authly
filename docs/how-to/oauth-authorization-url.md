# Construct an OAuth authorization URL

Use this recipe to build the URL that sends a user to Authly's OAuth authorization endpoint and to exchange the returned authorization code for an access token.

## Build the authorization URL

Call `authly.oauth.authorization_url()` with the provider name, redirect URI, and a state value:

```python
from authly import Authly

authly = Authly(project_id="proj_demo", api_key="key")

url = authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://app.example.com/callback",
    state="random-state-value",
)

print(url)
```

Output:

```text
https://auth.example.test/oauth/authorize?client_id=proj_demo&redirect_uri=https%3A%2F%2Fapp.example.com%2Fcallback&provider=github&state=random-state-value&response_type=code
```

Redirect the user to this URL. After authorization, the provider redirects back to your `redirect_uri` with an authorization `code` and the original `state`.

## Exchange the authorization code for a token

After the user authorizes and the provider redirects to your callback with a `code`, exchange it for an access token:

```python
token = authly.oauth.exchange_code(
    provider="github",
    code="auth_code_from_callback",
    redirect_uri="https://app.example.com/callback",
)

print(token.access_token)
print(token.user_id)
```

The `exchange_code` method:

- Validates that `provider`, `code`, and `redirect_uri` are non-empty (raises `ValidationError` otherwise)
- Creates a deterministic identity user per provider/code combination
- Returns a new `Token` with `token_type="access"`

### Identity user creation

Authly creates a reproducible identity user for each OAuth provider/code pair:

- Email format: `{provider}:{digest}@oauth.example.test` where `digest` is the first 12 characters of the SHA256 hash of the code
- Name: The capitalized provider name (e.g., "Github")
- Password: A random 32-character URL-safe string

The same provider/code pair always resolves to the same user within a client lifetime.

## Error handling

`exchange_code` raises `ValidationError` when any required parameter is empty:

```python
from authly.errors import ValidationError

try:
    token = authly.oauth.exchange_code(
        provider="",
        code="auth_code_123",
        redirect_uri="https://app.example.com/callback",
    )
except ValidationError as e:
    print(e)  # "provider is required"
```

## Complete OAuth flow example

```python
from authly import Authly
from authly.errors import ValidationError

authly = Authly(project_id="proj_demo", api_key="key")

# Step 1: Build authorization URL
auth_url = authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://app.example.com/callback",
    state="csrf-protection-state",
)
# Redirect user to auth_url...

# Step 2: After callback, exchange code for token
code = "code_from_callback"  # Extract from callback request
state = "state_from_callback"  # Verify matches original state

try:
    token = authly.oauth.exchange_code(
        provider="github",
        code=code,
        redirect_uri="https://app.example.com/callback",
    )
    print(f"Access token: {token.access_token}")
    print(f"User ID: {token.user_id}")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Limitations

- PKCE (Proof Key for Code Exchange) is not implemented in version 0.1
- The OAuth code is single-use: exchanging it creates a token but does not invalidate the code

## References

- [OAuthClient API](../reference/api.md#oauthclient)
- [Security notes](../explanation/security.md)
- `docs/reference/api.md`
- `docs/reference/sdk.md`
- `docs/explanation/faq.md`
- `docs/explanation/security.md`
- `docs/how-to/troubleshoot-errors.md`
- `src/authly/oauth.py`
- `tests/test_oauth.py`
- `CHANGELOG.md`
- `https://github.com/TheGreatBonnie/authly/pull/44`
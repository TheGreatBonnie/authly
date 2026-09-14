# Construct an OAuth authorization URL and exchange the code

Use this recipe to build the URL that sends a user to Authly's OAuth authorization endpoint, then exchange the returned authorization code for an access token.

## Prerequisites

- The `authly` package installed ([Getting started](../tutorials/getting-started.md))
- A project ID and API key for your environment

## Step 1: Build the authorization URL

Call `authly.oauth.authorization_url()` with the provider name, redirect URI, and a state value:

```python
from authly import Authly

authly = Authly(project_id="proj_demo", api_key="key")

url = authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://example.com/callback",
    state="demo-state",
)

print(url)
```

Output (single line):

```text
https://auth.example.test/oauth/authorize?client_id=proj_demo&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&provider=github&state=demo-state&response_type=code
```

Redirect the user to this URL. After authorization, the provider redirects back to your `redirect_uri` with an authorization `code` and the same `state` you provided.

## Step 2: Exchange the authorization code for a token

After the user authorizes and the provider redirects to your callback, extract the `code` from the query parameters and call `authly.oauth.exchange_code()`:

```python
# In your callback handler (example)
code = request.query_params.get("code")  # e.g., "auth_code_123"

if not code:
    raise ValueError("Authorization code missing")

token = authly.oauth.exchange_code(
    provider="github",
    code=code,
    redirect_uri="https://example.com/callback",
)

print(token.token)  # The access token string
print(token.user_id)  # The OAuth identity user ID
```

## How it works

`exchange_code()` performs the following:

1. **Validates inputs** — raises `ValidationError` if `provider`, `code`, or `redirect_uri` is empty.
2. **Creates a deterministic identity user** — keyed by a SHA-256 digest of the code (first 12 characters), not the raw code. The email format is `{provider}:{digest}@oauth.example.test`.
3. **Issues an access token** — returns a `Token` object with `token_type="access"` linked to the OAuth identity user.

The same `provider`/`code` pair always returns the same user within a client lifetime, making the flow deterministic and reversible.

## Validation errors

If any required argument is empty, `exchange_code()` raises `ValidationError`:

| Empty argument | Error message |
| -------------- | ------------- |
| `provider` | `provider is required` |
| `code` | `authorization code is required` |
| `redirect_uri` | `redirect_uri is required` |

## What's not implemented

PKCE (Proof Key for Code Exchange) is not implemented in version 0.1. It arrives in a later simulated release (v0.3.0 in `simulation/roadmap.md`).

## See also

- [OAuthClient API](../reference/api.md#oauthclient)
- [Security notes](../explanation/security.md)
- [Troubleshoot errors](troubleshoot-errors.md)

## References

- `docs/how-to/oauth-authorization-url.md`
- `docs/reference/api.md`
- `docs/explanation/faq.md`
- `docs/how-to/troubleshoot-errors.md`
- `src/authly/oauth.py`
- `tests/test_oauth.py`
- `https://github.com/TheGreatBonnie/authly/pull/41`
- `simulation/scenarios/001_add_oauth.md`
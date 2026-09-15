# Construct an OAuth authorization URL

Use this recipe to build the URL that sends a user to Authly's OAuth authorization endpoint, and to exchange the returned authorization code for an access token.

## Build the authorization URL

```python
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

## Exchange the authorization code for a token

After the user authorizes your application, the OAuth provider redirects them to your `redirect_uri` with an authorization `code`. Exchange this code for an access token:

```python
token = authly.oauth.exchange_code(
    provider="github",
    code="auth_code_from_callback",
    redirect_uri="https://example.com/callback",
)

print(token.access_token)
```

### How identity users are created

`exchange_code` creates a deterministic identity user for each unique `provider`/`code` pair:

1. The raw authorization code is never stored. Instead, Authly computes a SHA256 digest of the code and uses the first 12 characters as the identity key.
2. The user's email is constructed as `{provider}:{digest}@oauth.example.test` (for example, `github:a1b2c3d4e5f6@oauth.example.test`).
3. If a user with this email already exists, the existing user is used; otherwise, a new user is created with:
   - `name` set to the capitalized provider name (e.g., "Github")
   - A random 24-character password generated via `secrets.token_urlsafe(24)`

This design makes token issuance deterministic and reversible within a client lifetime: the same `provider`/`code` pair always yields the same user and a fresh token.

### Validation errors

`exchange_code` raises `ValidationError` if any required argument is empty:

- `provider is required` — when `provider` is an empty string
- `authorization code is required` — when `code` is an empty string  
- `redirect_uri is required` — when `redirect_uri` is an empty string

## Security notes

- The raw OAuth authorization code is never stored or logged; only its digest is used for identity lookup.
- The authorization code is single-purpose and is not reused as a credential (the generated password is random).
- PKCE is not implemented in version 0.1; it arrives in a later simulated release (v0.3.0 in `simulation/roadmap.md`).

## See also

- [OAuthClient API](../reference/api.md#oauthclient)
- [Security notes](../explanation/security.md)
- [Troubleshoot errors](troubleshoot-errors.md)

## References

- `docs/how-to/oauth-authorization-url.md`
- `docs/reference/api.md`
- `docs/explanation/security.md`
- `docs/how-to/troubleshoot-errors.md`
- `docs/explanation/faq.md`
- `CHANGELOG.md`
- `src/authly/oauth.py`
- `tests/test_oauth.py`
- `https://github.com/TheGreatBonnie/authly/pull/43`
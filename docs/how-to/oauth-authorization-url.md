---
title: Construct an OAuth authorization URL
description: Build the URL that initiates an OAuth login flow and exchange the authorization code for an access token.
---

# Construct an OAuth authorization URL

Use this recipe to build the URL that sends a user to Authly's OAuth authorization endpoint, and to exchange the returned authorization code for an access token.

## Build the authorization URL

Call `authorization_url` with the provider name, redirect URI, and a state value:

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

Redirect the user to this URL. After authorization, the provider redirects back to your `redirect_uri` with an authorization `code` and the `state` you provided.

## Exchange the authorization code for a token

After the user is redirected back to your application, exchange the authorization code for an access token:

```python
token = authly.oauth.exchange_code(
    provider="github",
    code="auth_code_from_callback",
    redirect_uri="https://example.com/callback",
)

print(token.token)
```

The `exchange_code` method:

- Validates that `provider`, `code`, and `redirect_uri` are non-empty (raises `ValidationError` otherwise)
- Creates a deterministic identity user per provider/code combination
- Returns a new access token bound to that user

## Version boundary

Version 0.1 supports constructing authorization URLs and exchanging authorization codes for access tokens. PKCE support arrives in a later simulated release (v0.3.0 in `simulation/roadmap.md`).

## See also

- [OAuthClient API](../reference/api.md#oauthclient)
- [Security notes](../explanation/security.md)
- [Troubleshoot errors](troubleshoot-errors.md)
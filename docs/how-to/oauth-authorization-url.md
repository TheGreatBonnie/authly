# OAuth

The initial Authly SDK can construct an OAuth authorization URL.

```python
url = authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://example.com/callback",
    state="demo-state",
)
```

The current benchmark implementation does not perform the authorization-code exchange.

PKCE is intentionally reserved for a later product version.

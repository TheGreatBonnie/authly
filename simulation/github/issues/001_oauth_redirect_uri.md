# Issue #201 — OAuth redirect URI documentation missing

**Status:** open  
**Author:** @dev-alice  
**Labels:** documentation, oauth

## Description

I'm trying to configure GitHub OAuth.

The documentation shows:

```python
authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://example.com/callback",
    state="demo-state",
)
```

But I can't find where the redirect URI is configured in the Authly dashboard.

## Expected

The OAuth documentation should explain:

- Where redirect URIs are configured.
- Which redirect URIs are allowed.
- Whether wildcards are supported.
- What happens when a redirect URI does not match.

## Environment

Authly 0.2.0

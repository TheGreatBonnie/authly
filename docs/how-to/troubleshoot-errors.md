# Troubleshoot errors

Work through the symptom you are seeing to find the cause and fix.

## Symptom: login fails with `AuthenticationError`

**Cause:** no registered user matches the email, or the password is wrong. The message is always `invalid email or password` and never says which part failed.

**Fix:** confirm the email exists via `authly.users.list()` and retry with that user's password. Remember that only the *first* user created with a given email can match a login.

```python
from authly import AuthenticationError

try:
    authly.auth.login(email="alice@example.com", password="secret")
except AuthenticationError:
    ...
```

## Symptom: permission check raises `AuthorizationError`

**Cause:** none of the roles assigned to the user contains the requested permission string. Permission names must match exactly (`documents:write` ≠ `documents:Write`).

**Fix:** inspect what the user actually holds, then assign a missing role or extend an existing one:

```python
held = authly.permissions.list_for_user(user_id=user.id)
print(sorted(held))
```

Note: this error also appears for unknown user IDs, because an unknown user has no assigned roles.

## Symptom: lookup raises `NotFoundError`

**Cause:** the ID passed to `users.get()`, `sessions.get()`, `sessions.revoke()`, `organizations.get()`, or `roles.get()` does not exist. IDs are generated per client instance and prefixed by type (`usr_`, `sess_`, `org_`, `role_`, `tok_`).

**Fix:** use the object returned when it was created, or check your prefix matches the resource type. All state is in-memory — objects created in another process (or before a restart) are gone.

## Symptom: creating a user raises `ValidationError`

**Cause:** the email is empty or contains no `@`, or the password is empty.

**Fix:** pass a syntactically valid email and a non-empty password.

```text
ValidationError: a valid email is required
ValidationError: password is required
```

## Symptom: initializing the client raises `ValueError`

**Cause:** `project_id` or `api_key` was omitted or empty.

**Fix:** see [Configure the client](configure-client.md).

## Symptom: OAuth flow stops after the redirect

**Cause:** the callback handler was not invoked, or the authorization code exchange failed. Common issues include:

- Missing or mismatched `redirect_uri` between `authorization_url()` and the provider callback configuration
- Missing `state` parameter in the callback URL (required for CSRF protection)
- Invalid or expired authorization code
- PKCE verifier mismatch (the code verifier must match the one generated during `authorization_url()`)

**Fix:** verify your callback handler is properly wired and the flow is completed:

```python
from authly import Authly

authly = Authly(
    project_id="proj_xxx",
    api_key="key_xxx",
    redirect_uri="http://localhost:8000/callback"
)

# 1. Generate the authorization URL (stores PKCE verifier internally)
url, state = authly.oauth.authorization_url(provider="google")

# 2. After user redirects back to your callback:
#    - Extract 'code' and 'state' from query parameters
#    - Call handle_callback with both values
result = authly.oauth.handle_callback(
    code="authorization_code_from_callback",
    state="state_from_callback"
)
# result contains access_token, refresh_token, expires_at, user_info
```

Ensure your `redirect_uri` matches exactly between the authorization URL generation and your OAuth provider's registered callback URL. The `state` parameter must be preserved through the redirect and passed to `handle_callback()`.

## Symptom: OAuth callback raises `OAuthError`

**Cause:** the authorization code exchange failed. This can happen when:

- The authorization code has expired (typically valid for a short time, e.g., 10 minutes)
- The code has already been used (codes are single-use)
- The PKCE code verifier does not match what was sent in the authorization request
- The `redirect_uri` does not match the one used in `authorization_url()`

**Fix:** restart the OAuth flow by generating a new authorization URL. Each flow generates a fresh PKCE verifier that must be used with its corresponding authorization code.

```python
from authly import OAuthError

try:
    result = authly.oauth.handle_callback(code=code, state=state)
except OAuthError as e:
    # Log the error and redirect user to restart OAuth flow
    print(f"OAuth failed: {e}")
    # Generate new authorization URL
    url, new_state = authly.oauth.authorization_url(provider="google")
```

## Still stuck?

Check the full [Errors reference](../reference/errors.md), or ask on the benchmark's issue tracker.

## References

- docs/how-to/troubleshoot-errors.md
- docs/how-to/oauth-authorization-url.md
- docs/reference/errors.md
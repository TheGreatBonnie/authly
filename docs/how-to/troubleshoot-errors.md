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

**Cause:** the OAuth callback handler is not configured, or the authorization code exchange failed. Common causes include:

- Missing or incorrect `redirect_uri` in the OAuth provider configuration
- The callback route is not implemented in your application
- PKCE verifier mismatch or missing `code_verifier` during token exchange
- The authorization code has expired (codes are typically valid for 10 minutes)
- The OAuth provider returned an error (user denied access, invalid scope, etc.)

**Fix:**

1. Verify your `redirect_uri` matches exactly what is registered with the OAuth provider (including protocol, domain, and path).

2. Implement the callback handler to exchange the authorization code for tokens:

```python
from authly import Authly

authly = Authly()

# In your callback route handler
def oauth_callback(request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    
    try:
        tokens = authly.oauth.exchange_code(
            code=code,
            redirect_uri="https://your-app.com/auth/callback",
            code_verifier=request.session.get("pkce_verifier")  # if using PKCE
        )
        # Store tokens and create session
        return {"access_token": tokens.access_token}
    except AuthenticationError as e:
        return {"error": str(e)}
```

3. If using PKCE, ensure the `code_verifier` is stored in the session when generating the authorization URL and passed to `exchange_code()`:

```python
import secrets

# When generating the authorization URL
verifier = secrets.token_urlsafe(32)
request.session["pkce_verifier"] = verifier

url = authly.oauth.authorization_url(
    provider="google",
    redirect_uri="https://your-app.com/auth/callback",
    pkce_verifier=verifier
)
```

4. Check for OAuth provider errors in the callback query parameters:

```python
error = request.query_params.get("error")
error_description = request.query_params.get("error_description")
if error:
    raise AuthenticationError(f"OAuth error: {error} - {error_description}")
```

For complete OAuth implementation details, see [OAuth authorization URL](oauth-authorization-url.md).

## Still stuck?

Check the full [Errors reference](../reference/errors.md), or ask on the benchmark's issue tracker.

## References

- docs/how-to/troubleshoot-errors.md
- docs/how-to/oauth-authorization-url.md
- docs/reference/errors.md
# Troubleshoot errors

Common error symptoms and how to recover from them.

## Symptom: `ValidationError: email is required`

**Cause:** `UserService.create()` received an empty email.

**Fix:** pass a non-empty string for `email`.

## Symptom: `ValidationError: name is required`

**Cause:** `UserService.create()` received an empty name.

**Fix:** pass a non-empty string for `name`.

## Symptom: `ValidationError: password is required`

**Cause:** `UserService.create()` received an empty password.

**Fix:** pass a non-empty string for `password`.

## Symptom: `NotFoundError` when getting a user

**Cause:** the user ID does not exist.

**Fix:** check the ID or create the user first.

## Symptom: `AuthenticationError` on login

**Cause:** email or password does not match.

**Fix:** verify credentials or create the user.

## Symptom: `ValidationError: project_id is required`

**Cause:** `Authly` was initialized without a `project_id`.

**Fix:** see [Configure the client](configure-client.md).

## Symptom: `ValidationError: api_key is required`

**Cause:** `Authly` was initialized without an `api_key`.

**Fix:** see [Configure the client](configure-client.md).

## Symptom: exchanging a code raises `ValidationError`

**Cause:** `provider`, `code`, or `redirect_uri` was empty when calling `exchange_code()`.

**Fix:** pass all three keyword arguments. Each is required — see [Construct an OAuth authorization URL](oauth-authorization-url.md).

## Still stuck?

Open an issue with:

1. The full error message and traceback.
2. The code that triggered it (redact credentials).
3. What you expected to happen.

## References

- `docs/how-to/troubleshoot-errors.md`
- `docs/how-to/oauth-authorization-url.md`
- `src/authly/oauth.py`
- `https://github.com/TheGreatBonnie/authly/pull/43`
# Troubleshoot errors

Work through the symptom you are seeing to find the cause and fix. The full exception catalog is at the bottom of this page.

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

**Cause:** the ID passed to `users.get()`, `sessions.get()`, `sessions.revoke()`, `organizations.get()`, `organizations.add_member()`, `roles.get()`, or `roles.assign()` does not exist. IDs are generated per client instance and prefixed by type (`usr_`, `sess_`, `org_`, `role_`, `tok_`).

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

**Fix:** see [Authentication](authentication.md).

## Symptom: OAuth flow stops after the redirect

**Cause:** version 0.1 has no callback handling, authorization-code exchange, or PKCE support. `authorization_url()` is the entire OAuth surface.

**Fix:** nothing to fix — the capability is not implemented yet. Track the roadmap in `simulation/roadmap.md`.

## Still stuck?

Ask on the benchmark's issue tracker at `simulation/github/issues/`.

## Error reference

All Authly exceptions derive from `AuthlyError`, which is exported at the package root alongside its subclasses.

```text
AuthlyError
├── AuthenticationError   login failed
├── AuthorizationError    permission check failed
├── NotFoundError         unknown resource ID
└── ValidationError       invalid input at creation time
```

### Hierarchy

| Exception              | Raised by                                                                 | Meaning                                                        |
| ---------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `AuthlyError`          | —                                                                         | Base class; catch this to handle any SDK error                 |
| `AuthenticationError`  | `auth.login()`                                                            | Unknown email or wrong password                                |
| `AuthorizationError`   | `permissions.check()`                                                     | No assigned role contains the requested permission             |
| `NotFoundError`        | `users.get()`, `sessions.get()`, `sessions.revoke()`, `organizations.get()`, `organizations.add_member()`, `roles.get()`, `roles.assign()` | Resource ID does not exist |
| `ValidationError`      | `users.create()`                                                          | Empty/malformed email or empty password                        |

### Not raised

- `ValueError` from client construction is **not** an `AuthlyError` — it is a plain Python error for misconfiguration.
- `permissions.list_for_user()` never raises, even for unknown users.
- Duplicate emails, role assignments, and organization memberships do not raise; sets absorb duplicates.

### Message formats

| Exception             | Example message                                    |
| --------------------- | -------------------------------------------------- |
| `AuthenticationError` | `invalid email or password`                        |
| `AuthorizationError`  | `user 'usr_...' lacks permission 'documents:write'` |
| `NotFoundError`       | `user 'usr_...' was not found`                     |
| `ValidationError`     | `a valid email is required` / `password is required` |

## See also

- [Authentication](authentication.md) — login and session recipes
- [Concepts](../explanation/concepts.md) — the security posture behind these defaults
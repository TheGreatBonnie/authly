# Errors

All Authly exceptions derive from `AuthlyError`, which is exported at the package root alongside its subclasses.

```text
AuthlyError
├── AuthenticationError   login failed
├── AuthorizationError    permission check failed
├── NotFoundError         unknown resource ID
├── ValidationError       invalid input at creation time
└── OAuthError            OAuth flow error
```

## Hierarchy

| Exception              | Raised by                                                                 | Meaning                                                        |
| ---------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------- |
| `AuthlyError`          | —                                                                         | Base class; catch this to handle any SDK error                 |
| `AuthenticationError`  | `auth.login()`                                                            | Unknown email or wrong password                                |
| `AuthorizationError`   | `permissions.check()`                                                     | No assigned role contains the requested permission             |
| `NotFoundError`        | `users.get()`, `sessions.get()`, `sessions.revoke()`, `organizations.get()`, `organizations.add_member()`, `roles.get()`, `roles.assign()` | Resource ID does not exist |
| `ValidationError`      | `users.create()`                                                          | Empty/malformed email or empty password                        |
| `OAuthError`           | `oauth.get_authorization_url()`, `oauth.handle_callback()`                | OAuth provider error, invalid state, or token exchange failure   |

## Not raised

- `ValueError` from client construction is **not** an `AuthlyError` — it is a plain Python error for misconfiguration.
- `permissions.list_for_user()` never raises, even for unknown users.
- Duplicate emails, role assignments, and organization memberships do not raise; sets absorb duplicates.

## Message formats

| Exception             | Example message                                    |
| --------------------- | -------------------------------------------------- |
| `AuthenticationError` | `invalid email or password`                        |
| `AuthorizationError`  | `user 'usr_...' lacks permission 'documents:write'` |
| `NotFoundError`       | `user 'usr_...' was not found`                     |
| `ValidationError`     | `a valid email is required` / `password is required` |
| `OAuthError`          | `oauth provider error: invalid state parameter` / `token exchange failed` |

## OAuth-specific errors

When working with OAuth providers, `OAuthError` provides additional context:

| Scenario | Error details |
|----------|---------------|
| Invalid or expired state parameter | `oauth provider error: invalid state parameter` |
| Authorization code exchange failure | `token exchange failed` |
| Missing or invalid provider configuration | `oauth provider error: configuration error` |
| User denied authorization | `oauth provider error: access denied` |

For recovery strategies per symptom, see [Troubleshoot errors](../how-to/troubleshoot-errors.md).
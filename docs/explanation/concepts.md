# Concepts

Two discussions in one place: how Authly decides whether a user may do something (the authorization model), and what its security posture is (what the benchmark guarantees, what it deliberately does not).

## The authorization model

This section explains why permission checks behave the way they do. For the step-by-step recipes, see [Authorization](../how-to/authorization.md).

### The three building blocks

Authorization in Authly has exactly three concepts:

1. **Permissions** — free-form strings, conventionally `resource:action` (for example `documents:write`). They exist only inside roles; there is no global permission registry.
2. **Roles** — named bundles of permissions. A role owns two sets: `permissions` and `assignments`.
3. **Assignment** — a user ID placed in a role's `assignments` set by `roles.assign()`.

```text
User ──(assigned to)──▶ Role ──(contains)──▶ Permission strings
```

### How a check resolves

`permissions.check(user_id, permission)` answers one question: *does any role that lists this user among its assignments contain this exact permission string?*

The algorithm is:

1. Collect every role whose `assignments` contains the user ID.
2. If any of those roles' `permissions` contains the exact string, return `True`.
3. Otherwise raise `AuthorizationError`.

Consequences worth internalizing:

- **Checks never return `False`.** Absence of permission is always an exception.
- **Unknown users fail checks.** A user ID with no role assignments — including one that was never created — raises `AuthorizationError`, not `NotFoundError`.
- **Matching is exact.** Permission strings are case-sensitive and compared literally; `documents:Write` does not satisfy `documents:write`.
- **Roles don't inherit.** There is no role hierarchy and no wildcard matching.

### What organizations do (and don't do)

Organizations group users into `member_ids`, but in version 0.1 they have no effect on authorization. Membership neither grants nor restricts anything. This separation is deliberate: it keeps v0.1 minimal while leaving room for organization-scoped permissions in later releases (planned for v0.5.0).

If you need "only members of Acme can edit documents" today, encode it as a role convention — create and assign roles per organization yourself.

### Why so simple?

Authly's purpose is to exercise documentation workflows against a realistic-but-small API. The flat role model covers the common RBAC vocabulary — grant, assign, check, list — without hiding the mechanics behind policy engines. Every question about *why* a check passed can be answered by inspecting two sets on a `Role`.

## The security posture

What Authly guarantees, what it deliberately does not, and how to work on it safely.

### What Authly is not

Authly is a fictional benchmark application. Its authentication primitives are intentionally simplified and must never guard real systems or real user data. Concrete simplifications include:

- Passwords are stored as provided, unhashed.
- API keys are accepted without validation beyond non-emptiness.
- Tokens are random strings with expiry metadata only; no signing, revocation lists, or rotation.
- OAuth stops at URL construction — no code exchange, no PKCE.

This is by design: real password hashing would add complexity without teaching anything new about documentation drift. Do not use Authly for production identity or security workloads.

### Working on the benchmark safely

Even fictional credentials should stay fictional:

- Do not commit real credentials anywhere in the repository.
- Use placeholder values (`proj_demo`, `demo_key`) in examples and tests.
- Treat webhook secrets as sensitive — examples use `webhook_secret`, nothing more.
- Never place real passwords in source control, including in test fixtures.

### Authentication changes are documentation events

In this repository, product changes to authentication are treated as high-impact documentation changes. When a release touches login, tokens, keys, or redirect validation, the affected guides and reference pages need review in the same change. The roadmap stages these deliberately — for example the v0.4.0 API-key deprecation introduces token-based client authentication and requires a migration guide.

If you are evolving Authly, read `simulation/roadmap.md` first and update the docs listed under each release's *Documentation risk* section alongside the code.

## FAQ

### Is Authly production-ready?

No. Authly is a fictional benchmark application for testing Draftly. Do not use it for production identity or security workloads.

### Does Authly support OAuth?

Version 0.1 constructs OAuth authorization URLs only. There is no callback handling, authorization-code exchange, or PKCE support yet. These arrive in later simulated releases (v0.2.0 and v0.3.0 in `simulation/roadmap.md`). See [Authentication](../how-to/authentication.md).

### Does Authly support roles and permissions?

Yes. Roles bundle permission strings and can be assigned to users; checks succeed when any assigned role contains the requested permission. See [the authorization model](#the-authorization-model).

### Do organizations grant permissions?

No. Organizations group users but play no part in authorization in version 0.1.

### Does Authly have persistent storage?

No. Everything lives in memory on the client instance and is lost when the process exits.

### How do I authenticate the client itself?

Initialize `Authly` with `project_id` and `api_key`. Both are required. Note that this is client configuration, separate from user login via `authly.auth.login()`. See [Authentication](../how-to/authentication.md).

### Why is my password stored in plain text?

Benchmark simplification, by design. See [What Authly is not](#what-authly-is-not).

### Where do I report issues?

Authly exists to exercise documentation workflows; its issue tracker lives at `simulation/github/issues/` within this repository.

## See also

- [Authorization](../how-to/authorization.md) — the recipes
- [Troubleshoot errors](../how-to/troubleshooting.md) — what each exception means in practice
- [API reference](../reference/api.md) — `PermissionService` and the data models
# Security

Authly is a fictional benchmark application. Its authentication primitives are intentionally simplified and **must not be used in production**.

## Known limitations

- Passwords are stored as provided, unhashed.
- API keys are accepted without validation beyond non-emptiness.
- Tokens are random strings with expiry metadata only; no signing, revocation lists, or rotation.
- OAuth supports building authorization URLs and exchanging codes for tokens; PKCE is not implemented.

## OAuth code exchange security

The `OAuthClient.exchange_code` method implements the following security measures:

### Code protection

The raw OAuth authorization code is **never stored or logged**. Instead:

1. A SHA256 digest of the code is computed
2. Only the first 12 characters of the digest are used as the identity key
3. The original code cannot be recovered from the stored digest

### Identity user format

OAuth identity users are created with emails in the format:

```
{provider}:{digest}@oauth.example.test
```

For example: `github:a1b2c3d4e5f6@oauth.example.test`

This format:
- Encodes the provider and code digest in the email
- Never includes the raw authorization code
- Enables deterministic user lookup for the same provider/code pair

### Single-purpose codes

The OAuth authorization code is single-purpose:
- It is not reused as a credential
- The user's password is randomly generated via `secrets.token_urlsafe(24)`
- Each code exchange creates a fresh access token

### Deterministic identity

Token issuance is deterministic and reversible within a client lifetime:
- The same `provider`/`code` pair always yields the same identity user
- This enables idempotent token issuance without duplicate user creation

## Working on the benchmark safely

When extending Authly:

1. Do not add real credential handling.
2. Keep secrets out of logs and error messages.
3. Document any new security limitations explicitly.

## References

- `docs/explanation/security.md`
- `docs/how-to/oauth-authorization-url.md`
- `src/authly/oauth.py`
- `https://github.com/TheGreatBonnie/authly/pull/43`
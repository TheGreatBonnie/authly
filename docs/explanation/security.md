# Security

Authly is a reference implementation for learning and benchmarking, not a production-grade authentication system. This page explains the security model and its intentional limitations.

## Security model

Authly implements a simplified authentication and authorization system with the following characteristics:

### Authentication

- **Password-based login**: Users authenticate with username and password credentials.
- **Session management**: Sessions are created upon successful authentication and tracked via session tokens.
- **API key authentication**: Alternative authentication using API keys for programmatic access.
- **OAuth 2.0 URL construction**: Support for generating OAuth authorization URLs (without full OAuth flow implementation).

### Authorization

- **Role-based access control (RBAC)**: Permissions are granted through roles assigned to users.
- **Organization-scoped permissions**: Access controls can be scoped to specific organizations.
- **Permission checks**: Runtime verification of user permissions before allowing operations.

### Data protection

- **Token-based sessions**: Sessions use random token strings for identification.
- **Webhook signatures**: Webhook payloads include HMAC-SHA256 signatures for verification.

## What Authly is not

Authly is a fictional benchmark application. Its authentication primitives are intentionally simplified and must never guard real systems or real user data. Concrete simplifications include:

- Passwords are stored as provided, unhashed.
- API keys are accepted without validation beyond non-emptiness.
- Tokens are random strings with expiry metadata only; no signing or rotation.
- OAuth stops at URL construction — no code exchange, no PKCE.

## Best practices for production

If you are building a production authentication system, consider the following requirements that Authly does not implement:

1. **Password hashing**: Always hash passwords using strong, salted algorithms (e.g., bcrypt, Argon2, PBKDF2).
2. **Token security**: Use signed tokens (JWT) or encrypted session tokens with secure key management.
3. **Token lifecycle**: Implement token rotation and short expiration times.
4. **OAuth compliance**: Implement full OAuth 2.0 flows with PKCE for public clients and state parameter validation.
5. **Rate limiting**: Add rate limiting to prevent brute-force attacks on authentication endpoints.
6. **Audit logging**: Log all authentication and authorization events for security monitoring.
7. **Input validation**: Validate and sanitize all user inputs to prevent injection attacks.
8. **HTTPS enforcement**: Require TLS for all authentication traffic.

## References

- docs/explanation/security.md
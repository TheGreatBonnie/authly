# PR #134 — Add refresh-token rotation

**Status:** merged  
**Author:** @maya  
**Labels:** authentication, security  
**Milestone:** v0.6.0

## Title

feat: rotate refresh tokens

## Description

Refresh tokens are now rotated whenever they are exchanged.

### Changes

- Add refresh tokens.
- Rotate refresh tokens after successful exchange.
- Revoke previously used refresh tokens.
- Add configurable token expiration.

## Documentation impact

Affected:

- `docs/authentication.md`
- `docs/sessions.md`
- `docs/security.md`
- `docs/troubleshooting.md`

## Review comments

### @alex

Please make sure the documentation explains what happens when a refresh token is reused.

### @maya

We'll document the invalid-token response and recovery flow.

## Merge

Merged into `main`.

Release target: `v0.6.0`

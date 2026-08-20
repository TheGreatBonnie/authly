# PR #101 — Add OAuth authentication

**Status:** merged  
**Author:** @maya  
**Labels:** feature, authentication, oauth  
**Milestone:** v0.2.0

## Title

feat: add OAuth authentication

## Description

Adds the first OAuth authentication flow to Authly.

### Changes

- Add OAuth authorization URL generation.
- Support GitHub and Google providers.
- Add OAuth callback handling.
- Add authorization-code exchange.
- Add OAuth configuration to the project settings.

## Code impact

Affected areas:

- `src/authly/oauth.py`
- `src/authly/auth.py`
- `src/authly/client.py`
- `tests/test_oauth.py`

## Documentation impact

Likely affected:

- `docs/oauth.md`
- `docs/authentication.md`
- `docs/getting-started.md`
- `docs/troubleshooting.md`
- `docs/security.md`

## Review comments

### @alex

> Do we have documentation for configuring the redirect URI?

### @maya

Not yet. I'll add it in a follow-up.

### @sam

The SDK example should probably show the complete OAuth flow rather than only generating the authorization URL.

## Merge

Merged into `main`.

Release target: `v0.2.0`

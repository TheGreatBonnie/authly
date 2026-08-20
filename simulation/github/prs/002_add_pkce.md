# PR #108 — Add OAuth PKCE

**Status:** merged  
**Author:** @maya  
**Labels:** feature, oauth, security  
**Milestone:** v0.3.0

## Title

feat: add PKCE support to OAuth

## Description

Adds PKCE support to the OAuth authorization flow.

### Changes

- Add `code_verifier`.
- Add `code_challenge`.
- Add `code_challenge_method`.
- Validate PKCE during token exchange.
- Require PKCE for public clients.

## Documentation impact

Affected:

- `docs/oauth.md`
- `docs/security.md`
- `examples/oauth.py`
- `docs/troubleshooting.md`

## Review comments

### @jordan

The current OAuth documentation doesn't mention PKCE.

### @maya

Agreed. We'll need to update the OAuth guide and example.

### @alex

Please also add a troubleshooting section for invalid PKCE verification.

## Merge

Merged into `main`.

Release target: `v0.3.0`

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- OAuth authorization-code exchange (`OAuthClient.exchange_code`) with a
  deterministic, per-provider/code identity user.
  - Creates identity users with email format `{provider}:{digest}@oauth.example.test`
  - Uses SHA256 digest of the code (first 12 characters) — raw code never stored
  - Deterministic identity: same provider/code pair yields same user
  - Random password generation via `secrets.token_urlsafe(24)`
- Input validation for `provider`, `code`, and `redirect_uri` in the OAuth
  exchange.

## References

- `CHANGELOG.md`
- `docs/how-to/oauth-authorization-url.md`
- `docs/reference/api.md`
- `docs/explanation/security.md`
- `src/authly/oauth.py`
- `tests/test_oauth.py`
- `https://github.com/TheGreatBonnie/authly/pull/43`
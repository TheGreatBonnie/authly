# Authly product roadmap

The roadmap is deliberately incremental. Do not implement every item at once.

## v0.1.0 — Current

- users
- password authentication
- sessions
- organizations
- roles
- permissions
- OAuth authorization URL helper
- token primitive
- webhook signing

## v0.2.0 — OAuth

Planned:

- OAuth providers
- callback handling
- authorization-code exchange

Documentation risk:

- authentication guide
- OAuth guide
- getting started
- troubleshooting

## v0.3.0 — PKCE

Planned:

- PKCE
- code verifier
- code challenge

Documentation risk:

- OAuth examples
- security guidance
- SDK reference

## v0.4.0 — API-key deprecation

Planned:

- replace or restrict API-key authentication
- introduce a new token configuration

Documentation risk:

- README
- SDK guide
- configuration examples
- migration guide

## v0.5.0 — RBAC expansion

Planned:

- richer roles
- organization-scoped permissions
- custom roles

Documentation risk:

- authorization
- organizations
- roles
- permissions

## v0.6.0 — Token rotation

Planned:

- refresh tokens
- rotation
- expiration policies

Documentation risk:

- sessions
- authentication
- security
- troubleshooting

## v0.7.0 — SDK breaking change

Planned:

- SDK method renames
- revised initialization

Documentation risk:

- every code example using the renamed API

## v0.8.0 — Security changes

Planned:

- stricter redirect URI validation
- revised webhook signing behavior

Documentation risk:

- security
- OAuth
- webhooks
- troubleshooting

## v1.0.0 — Migration milestone

Planned:

- stable API
- migration documentation
- consolidated reference docs

# Scenario 002 — PKCE

## Change

Authly adds PKCE to the OAuth authorization flow.

## Documentation risk

Existing OAuth examples may omit required PKCE parameters.

## Draftly should detect

- outdated OAuth examples
- missing security guidance
- missing PKCE explanation

## Evaluation

An example should fail if it cannot construct the new required flow.

# PR #117 — Deprecate API keys

**Status:** merged  
**Author:** @sam  
**Labels:** breaking-change, authentication  
**Milestone:** v0.4.0

## Title

breaking: deprecate API-key client authentication

## Description

Authly is moving away from API-key authentication for application requests.

### Old API

```python
authly = Authly(
    project_id="proj_demo",
    api_key="demo_key",
)
```

### New API

```python
authly = Authly(
    project_id="proj_demo",
    token="demo_token",
)
```

### Migration

Existing applications must replace api_key with token.

### Documentation impact

Potentially affected:

- README.md
- docs/getting-started.md
- docs/api-keys.md
- docs/sdk.md
- docs/authentication.md
- all Python examples

## Review comment

### @alex

This is a breaking change.

We need a migration guide before the release.

### @sam

Agreed. Migration docs will be tracked separately.

### Merge

Merged into main.

Release target: v0.4.0

```

```

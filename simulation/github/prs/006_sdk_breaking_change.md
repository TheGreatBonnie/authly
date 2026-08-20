# PR #141 — Rename permission check API

**Status:** merged  
**Author:** @sam  
**Labels:** breaking-change, sdk  
**Milestone:** v0.7.0

## Title

breaking: rename permissions.check to permissions.evaluate

## Description

Rename the permission-checking method to better describe its behavior.

### Before

```python
authly.permissions.check(
    user_id=user.id,
    permission="documents:write",
)
```

### After

```python
authly.permissions.evaluate(
    user_id=user.id,
    permission="documents:write",
)
```

### Documentation impact

Search required for:

- README.md
- docs/
- examples/
- code snippets
- tutorials

## Review comment

### @alex

We should make sure every documentation example is updated.

## Merge

Merged into main.

Release target: v0.7.0

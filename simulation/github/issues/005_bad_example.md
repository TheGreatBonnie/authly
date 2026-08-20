# Issue #233 — Permission example is broken

**Status:** open  
**Author:** @dev-chris  
**Labels:** bug, documentation, sdk

## Description

The documentation currently uses:

```python
authly.permissions.check(...)
```

but the SDK exposes:

```python
authly.permissions.evaluate(...)
```

The example fails when copied.

## Expected

Update all affected examples and documentation references.

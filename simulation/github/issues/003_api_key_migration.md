# Issue #217 — API-key migration guide needed

**Status:** open  
**Author:** @dev-sam  
**Labels:** documentation, breaking-change

## Description

After upgrading to Authly `0.4.0`, my application still uses:

```python
Authly(
    project_id="proj_demo",
    api_key="demo_key",
)
```

The release notes say API keys are deprecated, but I cannot find the migration instructions.

## Expected

Documentation should clearly show:

Old configuration
↓
New configuration
↓
Credential migration
↓
Validation

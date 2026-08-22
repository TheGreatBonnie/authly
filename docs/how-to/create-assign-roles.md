# Roles

Roles bundle permissions.

```python
role = authly.roles.create(
    name="editor",
    permissions={
        "documents:read",
        "documents:write",
    },
)
```

Assign a role:

```python
authly.roles.assign(
    user_id=user.id,
    role_id=role.id,
)
```

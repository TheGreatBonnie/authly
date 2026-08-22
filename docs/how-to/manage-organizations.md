# Organizations

Organizations group users.

Create one:

```python
organization = authly.organizations.create(
    name="Acme",
)
```

Add a user:

```python
authly.organizations.add_member(
    organization_id=organization.id,
    user_id=user.id,
)
```

The initial implementation uses a simple membership set.

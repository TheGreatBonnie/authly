# Authorization

Use these recipes to manage organizations, define roles and permissions, and check whether a user may act.

## Manage organizations and members

Create an organization, add users to it, and read it back.

### Prerequisites

- An initialized client ([Authentication](authentication.md))
- User IDs for the members you want to add

### Create an organization

```python
organization = authly.organizations.create(name="Acme")

print(organization.id)          # org_2b9d41c7ae
print(organization.member_ids)  # set()
```

### Add a member

```python
organization = authly.organizations.add_member(
    organization_id=organization.id,
    user_id="usr_4f8a2c1b9d",
)

print(sorted(organization.member_ids))  # ['usr_4f8a2c1b9d']
```

`add_member()` returns the updated organization. Membership is stored as a set, so adding the same user twice has no additional effect.

Note that `add_member()` does not verify that the user exists — it records whatever user ID you pass.

### Look up an organization

```python
organization = authly.organizations.get("org_2b9d41c7ae")
```

An unknown organization ID raises `NotFoundError`.

## Create and assign roles

Define a role with a set of permissions and assign it to a user so that permission checks pass.

### Prerequisites

- An initialized client ([Authentication](authentication.md))
- A user ID to assign the role to

### Create a role

Permissions are free-form strings. The convention used across Authly docs is `resource:action`:

```python
role = authly.roles.create(
    name="editor",
    permissions={"documents:read", "documents:write"},
)

print(role.id)  # role_5c8f0a3d71
```

The `permissions` argument is optional; omit it to create an empty role:

```python
role = authly.roles.create(name="viewer")
```

### Assign the role to a user

```python
role = authly.roles.assign(
    user_id="usr_4f8a2c1b9d",
    role_id=role.id,
)

print(role.assignments)  # {'usr_4f8a2c1b9d'}
```

Assignments are stored as a set of user IDs on the role, so assigning twice has no additional effect. One role can be assigned to many users.

### Look up a role

```python
role = authly.roles.get("role_5c8f0a3d71")
```

An unknown role ID raises `NotFoundError`. There is no lookup by role name.

## Check user permissions

Check whether a user has a permission:

```python
authly.permissions.check(
    user_id=user.id,
    permission="documents:write",
)
```

`check()` returns `True` when one of the user's assigned roles contains the requested permission. Otherwise it raises `AuthorizationError`.

To see everything a user holds, use `permissions.list_for_user()`:

```python
held = authly.permissions.list_for_user(user_id=user.id)
print(sorted(held))
```

`list_for_user()` never raises and returns an empty set for unknown users.

## Membership is not authorization

In version 0.1, being a member of an organization grants no permissions. Authorization comes only from roles assigned through `authly.roles.assign()`. See [Authorization model](../explanation/concepts.md).

## See also

- [Concepts](../explanation/concepts.md) — why checks never return `False`
- [API reference](../reference/api.md) — `Role` and `Organization` data models
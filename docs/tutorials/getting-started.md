# Getting started

## Install

```bash
pip install authly
```

## Initialize the client

```python
from authly import Authly

authly = Authly(
    project_id="proj_demo",
    api_key="demo_key",
)
```

## Create a user

```python
user = authly.users.create(
    email="alice@example.com",
    name="Alice",
    password="secret",
)
```

## Authenticate

```python
session = authly.auth.login(
    email=user.email,
    password="secret",
)
```

## Next steps

- Learn about [authentication](authentication.md).
- Learn about [sessions](sessions.md).
- Explore [organizations](organizations.md).

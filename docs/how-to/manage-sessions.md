# Sessions

Successful password authentication creates a session.

```python
session = authly.auth.login(
    email="alice@example.com",
    password="secret",
)
```

Sessions have:

- an ID
- a user ID
- a creation timestamp
- an active state

Sessions can be revoked:

```python
authly.sessions.revoke(session.id)
```

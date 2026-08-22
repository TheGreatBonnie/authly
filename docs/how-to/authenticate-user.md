# Authentication

Authly 0.1 supports email/password authentication through the Python SDK.

```python
session = authly.auth.login(
    email="alice@example.com",
    password="secret",
)
```

A successful login returns a session.

Authentication failures raise `AuthenticationError`.

OAuth is available as an authorization URL helper. See [OAuth](oauth.md).

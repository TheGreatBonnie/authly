# Webhooks

Authly provides a small webhook signing helper.

```python
payload = {
    "event": "user.created",
    "user_id": "usr_123",
}

signature = authly.webhooks.sign(
    payload=payload,
    secret="webhook_secret",
)
```

Verify a received payload:

```python
valid = authly.webhooks.verify(
    payload=payload,
    signature=signature,
    secret="webhook_secret",
)
```

The benchmark implementation uses an HMAC-SHA256 signature.

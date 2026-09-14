# Authentication

Use these recipes to configure the Authly client and manage user authentication: client initialization, password login, direct session management, and OAuth authorization URL construction.

## Configure the client

Initialize an `Authly` client with a project ID and API key so you can call any service method.

### Prerequisites

- The `authly` package installed ([Getting started](../tutorials/getting-started.md))
- A project ID and API key for your environment

### Initialize the client

Both arguments are keyword-only and required:

```python
from authly import Authly

authly = Authly(
    project_id="proj_demo",
    api_key="demo_key",
)
```

### What happens on bad input

Missing or empty values raise `ValueError` before any service is created:

```text
ValueError: project_id is required
ValueError: api_key is required
```

Passing arguments positionally raises `TypeError` because both parameters are keyword-only:

```python
Authly("proj_demo", "demo_key")  # TypeError
```

### Access configuration later

The client stores both values as attributes:

```python
authly.project_id  # "proj_demo"
authly.api_key     # "demo_key"
```

The project ID is also reused as the OAuth `client_id` when constructing authorization URLs.

## Authenticate a user

Log a user in with email and password and obtain a session.

### Prerequisites

- An initialized client (above)
- A user created with `authly.users.create()`

### Log in

```python
session = authly.auth.login(
    email="alice@example.com",
    password="secret",
)

print(session.id)      # sess_7d21e5a09c
print(session.user_id) # usr_4f8a2c1b9d
print(session.active)  # True
```

A successful login creates a new session owned by the matching user.

### Handle failed logins

An unknown email or a wrong password raises `AuthenticationError` with the message `invalid email or password`. The error does not reveal which of the two was wrong:

```python
from authly import AuthenticationError

try:
    authly.auth.login(email="alice@example.com", password="oops")
except AuthenticationError as exc:
    print(f"login failed: {exc}")
```

### Email lookup behavior

`login()` matches against the first user registered with that email address. Creating two users with the same email is allowed, but only the first one can ever match a login. Avoid duplicate emails.

## Create and revoke sessions

Manage sessions directly: create one for an existing user, look it up, and revoke it.

### Prerequisites

- An initialized client (above)
- A user ID (sessions belong to a user)

### Create a session

`auth.login()` creates sessions as a side effect of a password login. You can also create one directly for a user who already exists:

```python
session = authly.sessions.create(user_id="usr_4f8a2c1b9d")

print(session.id)        # sess_7d21e5a09c
print(session.active)    # True
print(session.created_at)  # e.g. 2026-08-22 10:15:00+00:00
```

### Look up a session

```python
session = authly.sessions.get("sess_7d21e5a09c")
```

An unknown session ID raises `NotFoundError`.

### Revoke a session

Revoking sets `active` to `False` and returns the updated session:

```python
session = authly.sessions.revoke("sess_7d21e5a09c")

print(session.active)  # False
```

Revoking is idempotent in effect but raises `NotFoundError` if the session does not exist, because `revoke()` performs a `get()` first.

### List nothing, safely

There is no `list()` on the session service. Track session IDs yourself if you need to enumerate them; every returned `Session` object carries its `id`.

## Construct an OAuth authorization URL

Build the URL that sends a user to Authly's OAuth authorization endpoint.

### Prerequisites

- An initialized client (above)

### Build the URL

```python
url = authly.oauth.authorization_url(
    provider="github",
    redirect_uri="https://example.com/callback",
    state="demo-state",
)

print(url)
```

Output (single line):

```text
https://auth.example.test/oauth/authorize?client_id=proj_demo&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&provider=github&state=demo-state&response_type=code
```

### Parameters

| Parameter      | Required | Used as                              |
| -------------- | -------- | ------------------------------------ |
| `provider`     | yes      | `provider` query parameter           |
| `redirect_uri` | yes      | `redirect_uri` query parameter       |
| `state`        | yes      | `state` query parameter              |

The `client_id` query parameter is filled from `authly.project_id`, and `response_type` is always `code`.

### Choose an unpredictable state

The state value is echoed back by the provider after the redirect. Generate it with a random source and verify it on return to protect against CSRF:

```python
from secrets import token_urlsafe

state = token_urlsafe(16)
```

### Version boundary

Version 0.1 only constructs the URL. There is no callback handling, authorization-code exchange, or PKCE support yet — see [Troubleshoot](troubleshooting.md) if you were expecting a token.

## See also

- [API reference](../reference/api.md) — method inventory and data models
- [Concepts](../explanation/concepts.md) — treat keys as placeholders in this benchmark
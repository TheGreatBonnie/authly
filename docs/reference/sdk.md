# Python SDK

Initialize the SDK with a project ID and API key:

```python
from authly import Authly

authly = Authly(
    project_id="proj_demo",
    api_key="demo_key",
)
```

The current SDK exposes:

```text
authly.users
authly.auth
authly.sessions
authly.organizations
authly.roles
authly.permissions
authly.oauth
authly.tokens
authly.webhooks
```

The SDK is intentionally in-memory for deterministic benchmark tests.

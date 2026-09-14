# Authly Documentation

Authly is a fictional developer authentication and authorization platform used as a Draftly benchmark. It ships as a small in-memory Python SDK covering users, password authentication, sessions, organizations, roles and permissions, OAuth authorization URLs, tokens, and signed webhooks.

**Current version:** `0.1.0`

> Authly is not a production identity platform. Its primitives are intentionally simplified so that later simulated releases can evolve them.

## Tutorials

Learning-oriented lessons. Start here if you are new to Authly.

- [Getting started](tutorials/getting-started.md) — install the SDK and run a complete user, login, organization, and permission workflow end to end.

## How-to guides

Problem-oriented recipes. Use these when you know what you want to do.

- [Authentication](how-to/authentication.md) — configure the client, log a user in, manage sessions, and construct an OAuth authorization URL.
- [Authorization](how-to/authorization.md) — manage organizations, create and assign roles, and check user permissions.
- [Sign and verify webhook payloads](how-to/webhooks.md)
- [Troubleshoot errors](how-to/troubleshooting.md) — work through error symptoms and recover.

## Reference

Information-oriented descriptions of the machinery.

- [API reference](reference/api.md) — SDK overview, complete method inventory, data models, and CLI.

## Explanation

Understanding-oriented discussion of concepts and design decisions.

- [Concepts](explanation/concepts.md) — the authorization model, the security posture, and FAQ.
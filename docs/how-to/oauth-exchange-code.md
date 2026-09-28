---
title: Exchange OAuth Authorization Code for Access Token
description: Learn how to exchange an OAuth authorization code for an access token in Authly.
---

# Exchange OAuth Authorization Code for Access Token

After a user authorizes your application via the OAuth authorization URL, Authly redirects them back to your application with an authorization code. This guide shows you how to exchange that code for an access token.

## Prerequisites

- You have already obtained an authorization code from the OAuth authorization flow
- You have your client ID and client secret
- You know your redirect URI

## Exchange the Authorization Code

Send a POST request to the token endpoint with the authorization code.

### HTTP Request

```http
POST /oauth/token
Content-Type: application/x-www-form-urlencoded
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `grant_type` | string | Yes | Must be `authorization_code` |
| `code` | string | Yes | The authorization code received from the authorization server |
| `redirect_uri` | string | Yes | The same redirect URI used in the authorization request |
| `client_id` | string | Yes | Your application's client ID |
| `client_secret` | string | Yes | Your application's client secret |

### Example Request

```bash
curl -X POST https://api.authly.example/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=AUTH_CODE_FROM_CALLBACK" \
  -d "redirect_uri=https://your-app.example/callback" \
  -d "client_id=your_client_id" \
  -d "client_secret=your_client_secret"
```

## Token Response

On success, the token endpoint returns a JSON response containing the access token and related information.

### Success Response

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2ggdG9rZW4...",
  "scope": "read write"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `access_token` | string | The access token to use for API requests |
| `token_type` | string | The type of token, typically `Bearer` |
| `expires_in` | number | Token lifetime in seconds |
| `refresh_token` | string | Token used to obtain new access tokens when the current one expires |
| `scope` | string | The scopes granted for this token |

## Using the Access Token

Include the access token in the Authorization header of subsequent API requests:

```http
GET /api/user
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Error Handling

If the code exchange fails, the endpoint returns an error response.

### Error Response Format

```json
{
  "error": "invalid_grant",
  "error_description": "The provided authorization grant is invalid, expired, or revoked."
}
```

### Common Error Codes

| Error Code | Description |
|------------|-------------|
| `invalid_request` | The request is missing a required parameter or is malformed |
| `invalid_client` | Client authentication failed |
| `invalid_grant` | The authorization code is invalid, expired, or was already used |
| `unauthorized_client` | The client is not authorized to use this grant type |
| `unsupported_grant_type` | The grant type is not supported |

## Security Considerations

- Always use HTTPS for token requests
- Store client secrets securely and never expose them in client-side code
- Authorization codes are single-use and expire quickly (typically 10 minutes)
- Validate the `state` parameter in the callback to prevent CSRF attacks

## References

- `docs/how-to/oauth-authorization-url.md`
- `docs/reference/api.md`
- `docs/reference/errors.md`

# OAuth Login Flow

This guide walks you through implementing the OAuth 2.0 login flow in your application using Authly. The OAuth login flow allows users to authenticate with external identity providers (such as Google, GitHub, or custom OIDC providers) and obtain access tokens for accessing protected resources.

## Prerequisites

Before implementing the OAuth login flow, ensure you have:

- An Authly account with OAuth provider credentials configured
- A registered OAuth application with your identity provider (Google, GitHub, etc.)
- Your application's `client_id` and `client_secret` from the provider
- A configured redirect URI that matches your Authly setup

## Overview of the OAuth Login Flow

The OAuth login flow in Authly follows the standard Authorization Code grant type:

1. **Authorization Request**: Your application redirects the user to the identity provider's authorization endpoint
2. **User Consent**: The user authenticates with the provider and grants permissions
3. **Authorization Code**: The provider redirects back to your application with an authorization code
4. **Token Exchange**: Your application exchanges the code for access and refresh tokens
5. **Authenticated Session**: Use the access token to make authenticated requests

## Step 1: Generate the Authorization URL

First, generate an authorization URL to redirect the user to the identity provider:

```rust
use authly::oauth::{OAuthClient, AuthorizationRequest};

let client = OAuthClient::new(
    "your-client-id",
    "your-client-secret",
    "https://your-app.com/auth/callback",
);

let auth_url = client
    .authorize_url("https://accounts.google.com/o/oauth2/auth")
    .set_scope("openid email profile")
    .set_state("random-state-string")
    .build();

// Redirect the user to auth_url
```

The `state` parameter is required for CSRF protection. Store it in the session and validate it when the user returns.

## Step 2: Handle the Callback

When the user completes authentication, the provider redirects to your callback URL with an authorization code:

```rust
use authly::oauth::TokenRequest;

// Extract code and state from the callback request
let code = extract_code_from_request(&request)?;
let state = extract_state_from_request(&request)?;

// Validate the state parameter matches the stored value
if !validate_state(&state, &session_state) {
    return Err(Error::InvalidState);
}

// Exchange the authorization code for tokens
let token_response = client
    .exchange_code(code)
    .request()
    .await?;

let access_token = token_response.access_token;
let refresh_token = token_response.refresh_token;
let expires_in = token_response.expires_in;
```

## Step 3: Create or Update User Session

After obtaining tokens, create a session for the authenticated user:

```rust
use authly::session::{SessionManager, SessionConfig};

let session = SessionManager::create()
    .set_user_id(token_response.user_id)
    .set_access_token(access_token)
    .set_refresh_token(refresh_token)
    .set_expires_at(expires_in)
    .build();

// Store the session and set a session cookie
response.set_cookie("session_id", session.id);
```

## Step 4: Access Protected Resources

Use the access token to make authenticated API requests:

```rust
use authly::http::AuthenticatedClient;

let client = AuthenticatedClient::new(&access_token);
let user_info = client
    .get("https://api.provider.com/userinfo")
    .send()
    .await?;
```

## Configuration

Configure OAuth providers in your Authly configuration:

```toml
[oauth.providers.google]
client_id = "your-google-client-id"
client_secret = "your-google-client-secret"
redirect_uri = "https://your-app.com/auth/callback"
authorization_endpoint = "https://accounts.google.com/o/oauth2/auth"
token_endpoint = "https://oauth2.googleapis.com/token"
scopes = ["openid", "email", "profile"]

[oauth.providers.github]
client_id = "your-github-client-id"
client_secret = "your-github-client-secret"
redirect_uri = "https://your-app.com/auth/callback"
authorization_endpoint = "https://github.com/login/oauth/authorize"
token_endpoint = "https://github.com/login/oauth/access_token"
scopes = ["user:email", "read:user"]
```

## Error Handling

Handle common OAuth errors that may occur during the flow:

| Error | Cause | Resolution |
|-------|-------|------------|
| `invalid_request` | Missing or invalid parameters | Check request parameters |
| `invalid_client` | Invalid client credentials | Verify client_id and client_secret |
| `invalid_grant` | Expired or invalid authorization code | Restart the flow |
| `unauthorized_client` | Client not authorized for this grant type | Check provider configuration |
| `access_denied` | User denied authorization | Prompt user to retry |
| `unsupported_response_type` | Provider doesn't support the requested response type | Use `code` response type |
| `invalid_scope` | Requested scope is invalid or unknown | Check configured scopes |

## Security Considerations

- **PKCE**: Use PKCE (Proof Key for Code Exchange) for public clients
- **State Parameter**: Always validate the state parameter to prevent CSRF attacks
- **HTTPS**: Use HTTPS for all OAuth redirects and token exchanges
- **Token Storage**: Store tokens securely; never expose them in client-side code
- **Token Expiration**: Handle token expiration and implement refresh token logic

## Complete Example

Here's a complete example of an OAuth login handler:

```rust
use authly::oauth::{OAuthClient, TokenResponse};
use authly::session::SessionManager;

async fn handle_oauth_login(
    provider: &str,
    session: &mut Session,
) -> Result<Redirect, Error> {
    let config = get_provider_config(provider)?;
    let client = OAuthClient::from_config(&config)?;
    
    let state = generate_random_state();
    session.set("oauth_state", &state);
    
    let auth_url = client
        .authorize_url(&config.authorization_endpoint)
        .set_scope(&config.scopes.join(" "))
        .set_state(&state)
        .build();
    
    Ok(Redirect::to(auth_url))
}

async fn handle_oauth_callback(
    code: String,
    state: String,
    session: &Session,
) -> Result<Response, Error> {
    let stored_state = session.get("oauth_state")?;
    if state != stored_state {
        return Err(Error::InvalidState);
    }
    
    let config = get_provider_config(&session.provider)?;
    let client = OAuthClient::from_config(&config)?;
    
    let token_response = client
        .exchange_code(&code)
        .request()
        .await?;
    
    let user_session = SessionManager::create()
        .set_user_id(&token_response.user_id)
        .set_access_token(&token_response.access_token)
        .build();
    
    Ok(Response::redirect("/dashboard"))
}
```

## References

- [docs/how-to/oauth-authorization-url.md](docs/how-to/oauth-authorization-url.md)
- [docs/how-to/authenticate-user.md](docs/how-to/authenticate-user.md)
- [docs/how-to/manage-sessions.md](docs/how-to/manage-sessions.md)
- [docs/reference/api.md](docs/reference/api.md)
- [docs/reference/sdk.md](docs/reference/sdk.md)
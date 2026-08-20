# Troubleshooting

## Invalid email or password

`authly.auth.login()` raises `AuthenticationError` when the email or password does not match a stored user.

## Missing permission

`authly.permissions.check()` raises `AuthorizationError` when no assigned role contains the requested permission.

## OAuth callback

The current OAuth helper only creates the authorization URL. Token exchange is not implemented in version 0.1.

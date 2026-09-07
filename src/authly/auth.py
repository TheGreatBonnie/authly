"""Authentication service."""

from .errors import AuthenticationError
from .sessions import Session


class AuthService:
    def __init__(self, client):
        self.client = client

    def login(self, *, email: str, password: str) -> Session:
        user = next(
            (u for u in self.client._users.values() if u.email == email),
            None,
        )

        if user is None or user.password != password:
            raise AuthenticationError("invalid email or password")

        return self.client.sessions.create(user_id=user.id)

    def login_with_oauth(
        self,
        *,
        provider: str,
        code: str,
        redirect_uri: str,
    ) -> Session:
        """Complete the OAuth login flow: exchange a code for a token, then
        start a session for the OAuth identity."""
        token = self.client.oauth.exchange_code(
            provider=provider,
            code=code,
            redirect_uri=redirect_uri,
        )
        return self.client.sessions.create(user_id=token.user_id)

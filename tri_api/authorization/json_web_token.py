import jwt
from tri_api.support.enums import Access
from tri_api.models.tenant.user import User
from tri_api.support.config import CONFIGURATION
from fastapi_jwt import (
    JwtAccessBearer,
    JwtRefreshBearer,
    JwtAuthorizationCredentials,
)


access_security = JwtAccessBearer(
    CONFIGURATION.authorization_jwt_secret_key,
    access_expires_delta=Access.access_expires.value,
    refresh_expires_delta=Access.refresh_expires.value,
)

refresh_security = JwtRefreshBearer(
    CONFIGURATION.authorization_jwt_secret_key,
    access_expires_delta=Access.access_expires.value,
    refresh_expires_delta=Access.refresh_expires.value,
)


async def user_from_credentials(auth: JwtAuthorizationCredentials) -> User | None:
    """Return the user associated with auth credentials."""
    return await User.by_email(auth.subject["username"])


async def user_from_token(token: str) -> User | None:
    """Return the user associated with a token value."""
    payload = jwt.decode(
        token,
        CONFIGURATION.authorization_jwt_secret_key,
        algorithms=["HS256"],  # Using the default algorithm for JWT
    )
    return await User.by_email(payload["subject"]["username"])

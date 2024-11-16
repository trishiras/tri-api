from tri_api.models.tenant.user import User
from fastapi import HTTPException, Security
from tri_api.support.enums import ExceptionMessage
from fastapi_jwt import JwtAuthorizationCredentials
from tri_api.authorization.json_web_token import (
    access_security,
    user_from_credentials,
)


async def current_user(
    auth: JwtAuthorizationCredentials = Security(access_security),
) -> User:
    """Return the current authorized user."""
    if not auth:
        raise HTTPException(
            status_code=401,
            detail=ExceptionMessage.no_auth_cred_found.value,
        )

    user = await user_from_credentials(auth)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=ExceptionMessage.auth_user_not_found.value,
        )

    if user.email_confirmed_at is not None:
        raise HTTPException(
            status_code=400,
            detail=ExceptionMessage.email_already_verified.value,
        )

    if user.disabled:
        raise HTTPException(
            status_code=400,
            detail=ExceptionMessage.account_disabled.value,
        )

    if not user.is_member:
        raise HTTPException(
            status_code=400,
            detail=ExceptionMessage.not_a_member.value,
        )

    return user


async def current_user_to_modify(
    auth: JwtAuthorizationCredentials = Security(access_security),
) -> User:
    """Return the current authorized user."""
    if not auth:
        raise HTTPException(
            status_code=401,
            detail=ExceptionMessage.no_auth_cred_found.value,
        )

    user = await user_from_credentials(auth)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail=ExceptionMessage.auth_user_not_found.value,
        )

    return user

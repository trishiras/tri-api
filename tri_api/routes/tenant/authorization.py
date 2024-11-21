from tri_api.support.password import hash_password
from fastapi_jwt import JwtAuthorizationCredentials
from tri_api.models.tenant.user import User, UserAuth
from fastapi import APIRouter, HTTPException, Security
from tri_api.models.tenant.authorization import AccessToken, RefreshToken
from tri_api.support.enums import RouteEnum, ResponseCode, ExceptionMessage
from tri_api.authorization.json_web_token import access_security, refresh_security


router = APIRouter(
    prefix=RouteEnum.api.value + RouteEnum.authorization.value,
    tags=["Auth"],
)


@router.post(RouteEnum.login.value)
async def login(user_auth: UserAuth) -> RefreshToken:
    """Authenticate and returns the user's JWT."""
    user = await User.by_email(user_auth.email)
    if user is None or hash_password(user_auth.password) != user.password:
        raise HTTPException(
            status_code=ResponseCode.unauthorized.value,
            detail=ExceptionMessage.invalid_credentials.value,
        )
    # if user.email_confirmed_at is None:
    #     raise HTTPException(
    #         status_code=ResponseCode.bad_request.value,
    #         detail=ExceptionMessage.unconfirmed_email.value,
    #     )
    # if user.disabled:
    #     raise HTTPException(
    #         status_code=ResponseCode.bad_request.value,
    #         detail=ExceptionMessage.account_disabled.value,
    #     )
    access_token = access_security.create_access_token(user.jwt_subject)
    refresh_token = refresh_security.create_refresh_token(user.jwt_subject)
    return RefreshToken(access_token=access_token, refresh_token=refresh_token)


@router.post(RouteEnum.refresh.value)
async def refresh(
    auth: JwtAuthorizationCredentials = Security(refresh_security),
) -> AccessToken:
    """Return a new access token from a refresh token."""
    access_token = access_security.create_access_token(subject=auth.subject)
    return AccessToken(access_token=access_token)

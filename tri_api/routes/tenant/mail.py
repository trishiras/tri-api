from pydantic import EmailStr
from datetime import datetime, UTC
from tri_api.models.tenant.user import User
from tri_api.support.mail import send_verification_email
from fastapi import (
    Body,
    Response,
    APIRouter,
    HTTPException,
)
from tri_api.support.enums import (
    RouteEnum,
    ResponseCode,
    ExceptionMessage,
)
from tri_api.authorization.json_web_token import (
    access_security,
    user_from_token,
)


router = APIRouter(
    prefix=RouteEnum.api.value + RouteEnum.mail.value,
    tags=["Mail"],
)


@router.post(RouteEnum.verify.value)
async def request_verification_email(
    email: EmailStr = Body(..., embed=True)
) -> Response:
    """Send the user a verification email."""
    user = await User.by_email(email)
    if user is None:
        raise HTTPException(
            status_code=ResponseCode.not_found.value,
            detail=ExceptionMessage.user_not_found.value,
        )
    if user.email_confirmed_at is not None:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.email_already_verified.value,
        )
    if user.disabled:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.account_disabled.value,
        )
    token = access_security.create_access_token(user.jwt_subject)
    await send_verification_email(email, token)
    return Response(status_code=ResponseCode.success.value)


@router.post(RouteEnum.verify_token.value)
async def verify_email(token: str) -> Response:
    """Verify the user's email with the supplied token."""
    user = await user_from_token(token)
    if user is None:
        raise HTTPException(
            status_code=ResponseCode.not_found.value,
            detail=ExceptionMessage.user_not_found.value,
        )
    if user.email_confirmed_at is not None:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.email_already_verified.value,
        )
    if user.disabled:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.account_disabled.value,
        )
    user.email_confirmed_at = datetime.now(tz=UTC)
    await user.save()
    return Response(status_code=ResponseCode.success.value)

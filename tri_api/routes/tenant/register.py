from pydantic import EmailStr
from tri_api.support.password import hash_password
from tri_api.support.mail import send_password_reset_email
from tri_api.support.current_user import current_user_to_modify
from tri_api.models.tenant.user import (
    User,
    UserAuth,
    UserPublic,
)
from tri_api.models.tenant.tenant import (
    InviteToken,
    InviteTokenInput,
)
from fastapi import (
    APIRouter,
    Depends,
    Body,
    HTTPException,
    Response,
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
    prefix=RouteEnum.api.value + RouteEnum.register.value,
    tags=["Register"],
)


embed = Body(..., embed=True)


@router.post("", response_model=UserPublic)
async def user_registration(user_auth: UserAuth):
    """Create a new user."""
    user = await User.by_email(user_auth.email)
    if user is not None:
        raise HTTPException(
            status_code=ResponseCode.conflict.value,
            detail=ExceptionMessage.user_already_exists.value,
        )

    if user_auth.invite_token is not None:
        invite_token = await InviteToken.by_token(user_auth.invite_token)
        if invite_token is None:
            raise HTTPException(
                status_code=ResponseCode.bad_request.value,
                detail=ExceptionMessage.invalid_invite_token.value,
            )

        hashed = hash_password(user_auth.password)
        user = User(email=user_auth.email, password=hashed)
        await user.create()
        await invite_token.assign_user(user_auth.invite_token, user.id)
        user.is_member = True
        await user.save()
        return user

    hashed = hash_password(user_auth.password)
    user = User(email=user_auth.email, password=hashed)
    await user.create()

    return user


@router.post(RouteEnum.forgot_password.value)
async def forgot_password(email: EmailStr = embed) -> Response:
    """Send password reset email."""
    user = await User.by_email(email)
    if user is None:
        raise HTTPException(
            status_code=ResponseCode.not_found.value,
            detail=ExceptionMessage.user_not_found.value,
        )
    if user.email_confirmed_at is None:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.unconfirmed_email.value,
        )
    if user.disabled:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.account_disabled.value,
        )
    token = access_security.create_access_token(user.jwt_subject)
    await send_password_reset_email(email, token)
    return Response(status_code=ResponseCode.success.value)


@router.post(RouteEnum.reset_password.value, response_model=UserPublic)
async def reset_password(token: str, password: str = embed):
    """Reset user password from token value."""
    user = await user_from_token(token)
    if user is None:
        raise HTTPException(
            status_code=ResponseCode.not_found.value,
            detail=ExceptionMessage.user_not_found.value,
        )
    if user.email_confirmed_at is None:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.unconfirmed_email.value,
        )
    if user.disabled:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.account_disabled.value,
        )
    user.password = hash_password(password)
    await user.save()
    return user


@router.post(RouteEnum.add_invite.value)
async def add_invite(
    invite_token_input: InviteTokenInput,
    user: User = Depends(current_user_to_modify),
) -> Response:
    """Verify the user's email with the supplied token."""

    if user is None:
        raise HTTPException(
            status_code=ResponseCode.not_found.value,
            detail=ExceptionMessage.user_not_found.value,
        )
    if user.is_member:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.account_already_active.value,
        )

    invite_token = await InviteToken.by_token(invite_token_input.invite_token)
    if invite_token is None:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.invalid_invite_token.value,
        )

    await invite_token.assign_user(invite_token.token, user.id)
    user.is_member = True
    await user.save()

    return Response(status_code=ResponseCode.success.value)


@router.post(RouteEnum.activate.value)
async def activate(
    invite_token_input: InviteTokenInput,
    user: User = Depends(current_user_to_modify),
) -> Response:
    """Verify the user's email with the supplied token."""

    if user is None:
        raise HTTPException(
            status_code=ResponseCode.not_found.value,
            detail=ExceptionMessage.user_not_found.value,
        )
    if not user.disabled:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.account_already_active.value,
        )

    invite_token = await InviteToken.by_token(invite_token_input.invite_token)
    if invite_token is None:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.invalid_invite_token.value,
        )

    old_token = await InviteToken.by_user(user.id)
    if old_token is not None:
        if old_token.token == invite_token.token:
            raise HTTPException(
                status_code=ResponseCode.bad_request.value,
                detail=ExceptionMessage.invalid_invite_token.value,
            )

    await invite_token.assign_user(invite_token.token, user.id)
    user.is_member = True
    user.disabled = False
    await user.save()

    return Response(status_code=ResponseCode.success.value)

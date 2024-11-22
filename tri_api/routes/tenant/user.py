from tri_api.models.tenant.tenant import InviteToken
from fastapi_jwt import JwtAuthorizationCredentials
from tri_api.support.current_user import current_user
from tri_api.authorization.json_web_token import access_security
from tri_api.models.tenant.user import (
    User,
    UserPublic,
    UserUpdate,
)
from fastapi import (
    Depends,
    Response,
    Security,
    APIRouter,
    HTTPException,
)
from tri_api.support.enums import (
    RouteEnum,
    ResponseCode,
    ExceptionMessage,
)


router = APIRouter(
    prefix=RouteEnum.api.value + RouteEnum.user.value,
    tags=["User"],
)


@router.get("", response_model=UserPublic)
async def get_user(user: User = Depends(current_user)):
    """Return the current user."""
    return user


@router.patch("", response_model=UserPublic)
async def update_user(update: UserUpdate, user: User = Depends(current_user)):
    fields = update.model_dump(exclude_unset=True)
    if new_email := fields.pop("email", None):
        if new_email != user.email:
            if await User.by_email(new_email) is not None:
                raise HTTPException(
                    status_code=ResponseCode.bad_request.value,
                    detail=ExceptionMessage.email_already_exists.value,
                )
            user.update_email(new_email)
    user = user.model_copy(update=fields)
    await user.save()
    return user


@router.delete("")
async def delete_user(
    auth: JwtAuthorizationCredentials = Security(access_security),
) -> Response:
    """Delete current user."""
    user = await User.by_email(auth.subject["username"])
    invite_token = await InviteToken.by_user(user.id)
    invite_token.user = None

    await invite_token.save()

    await user.delete()
    return Response(status_code=ResponseCode.no_content.value)

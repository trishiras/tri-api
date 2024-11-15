from fastapi import HTTPException
from tri_api.support.config import CONFIGURATION
from tri_api.support.password import hash_password
from tri_api.support.enums import (
    ResponseCode,
    ExceptionMessage,
)
from tri_api.models.super.user import (
    SuperUser,
    SuperUserLogin,
)


async def current_super_user(super_user_login: SuperUserLogin) -> SuperUser:
    if not (
        super_user_login.id and super_user_login.password and super_user_login.login_key
    ):
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.super_user_exception.value,
        )

    if super_user_login.login_key != CONFIGURATION.super_user_login_key:
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.super_user_exception.value,
        )

    super_user = await SuperUser.by_id(super_user_login.id)
    if not super_user:
        raise HTTPException(
            status_code=ResponseCode.bad_gateway.value,
            detail=ExceptionMessage.super_user_exception.value,
        )
    if super_user.password != hash_password(super_user_login.password):
        raise HTTPException(
            status_code=ResponseCode.bad_gateway.value,
            detail=ExceptionMessage.super_user_exception.value,
        )

    return super_user

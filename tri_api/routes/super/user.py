from tri_api.support.config import CONFIGURATION
from tri_api.support.password import hash_password
from fastapi import APIRouter, Depends, HTTPException, Response, Security
from tri_api.support.enums import RouteEnum, ResponseCode, ExceptionMessage
from tri_api.models.super.user import (
    SuperUser,
    SuperUserAuth,
    SuperUserResponse,
)


router = APIRouter(
    prefix=RouteEnum.api.value + RouteEnum.super_user.value,
    tags=["SuperUser"],
)


@router.post(RouteEnum.register.value, response_model=SuperUserResponse)
async def create_super_user(super_user_auth: SuperUserAuth) -> SuperUserResponse:
    if not (
        super_user_auth.secret_key
        and super_user_auth.secret_token
        and super_user_auth.secret_password
    ):
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.super_user_exception.value,
        )

    if (super_user_auth.secret_key != CONFIGURATION.super_user_secret_key) and (
        super_user_auth.secret_token != CONFIGURATION.super_user_secret_token
    ):
        raise HTTPException(
            status_code=ResponseCode.bad_request.value,
            detail=ExceptionMessage.super_user_exception.value,
        )

    hashed = hash_password(super_user_auth.secret_password)
    super_user = SuperUser(password=hashed)
    await super_user.create()
    return super_user

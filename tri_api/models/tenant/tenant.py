from uuid import uuid4
from typing import Optional, List
from fastapi import HTTPException
from beanie import Indexed, Document
from pydantic import Field, BaseModel
from tri_api.support.enums import ResponseCode, ExceptionMessage


class InviteTokenInput(BaseModel):
    invite_token: str


class InviteToken(Document):
    id: str = Field(default_factory=lambda: str(uuid4().hex))
    user: Optional[str] = Field(default=None)
    token: Indexed(str, unique=True)
    status: bool = Field(default=True)

    class Settings:
        name = "invite_token"
        # use_cache = True
        indexes = [
            "id",
        ]

    @classmethod
    async def by_id(cls, id: str) -> Optional["InviteToken"]:
        return await cls.find_one(cls.id == id)

    @classmethod
    async def by_user(cls, user: str) -> Optional["InviteToken"]:
        return await cls.find_one(cls.user == user)

    @classmethod
    async def by_token(cls, token: str) -> Optional["InviteToken"]:
        return await cls.find_one(cls.token == token)

    @classmethod
    async def assign_user(cls, token: str, user: str) -> Optional["InviteToken"]:
        invite_token = await cls.by_token(token)
        if invite_token is None:
            return invite_token

        if invite_token.user:
            raise HTTPException(
                status_code=ResponseCode.bad_request.value,
                detail=ExceptionMessage.invalid_invite_token.value,
            )

        has_token = await cls.by_user(user)
        if has_token:
            has_token.user = None
            await has_token.save()

        invite_token.user = user
        await invite_token.save()
        return invite_token


class ActiveTokenList(BaseModel):
    token_list: List[str]

    @classmethod
    async def get_token_list(cls) -> "ActiveTokenList":
        tokens = await InviteToken.find(
            InviteToken.status == True,
            InviteToken.user == None,
        ).to_list()

        token_list = []
        for token in tokens:
            token_list.append(token.token)
        return cls(token_list=token_list)

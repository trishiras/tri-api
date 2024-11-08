from uuid import uuid4
from typing import Optional
from beanie import Document
from pydantic import Field, BaseModel


class SuperUserAuth(BaseModel):
    secret_key: str
    secret_token: str
    secret_password: str


class SuperUserLogin(BaseModel):
    id: str
    password: str
    login_key: str


class SuperUserResponse(BaseModel):
    id: str


class SuperUser(Document):
    id: str = Field(default_factory=lambda: str(uuid4().hex))
    password: str

    @classmethod
    async def by_id(cls, id: str) -> Optional["SuperUser"]:
        return await cls.find_one(cls.id == id)


class SuperUserMemberUpdate(SuperUserLogin):
    user_id: Optional[str] = Field(default=None)
    disable: Optional[str] = Field(default=None)

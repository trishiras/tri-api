from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from beanie import Document, Indexed
from typing import Annotated, Any, Optional
from pydantic import Field, BaseModel, EmailStr
from tri_api.support.enums import ResponseCode, ExceptionMessage


class UserAuth(BaseModel):
    """User register and login auth."""

    email: EmailStr
    password: str
    invite_token: Optional[str] = Field(default=None)


class UserUpdate(BaseModel):
    """Updatable user fields."""

    email: Optional[EmailStr] = Field(unique=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class UserPublic(UserUpdate):
    """User fields returned to the client."""

    email: Annotated[str, Indexed(EmailStr, unique=True)]
    disabled: bool = False
    is_member: bool = False


class User(Document, UserPublic):
    """User DB representation."""

    id: str = Field(default_factory=lambda: str(uuid4().hex))
    password: str
    email_confirmed_at: Optional[datetime] = Field(default=None)

    class Settings:
        name = "user"
        # use_cache = True
        indexes = []

    def __repr__(self) -> str:
        return f"<User {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, User):
            return self.email == other.email
        return False

    @property
    def created(self) -> datetime | None:
        """Datetime user was created from ID."""
        return self.id.generation_time if self.id else None

    @property
    def jwt_subject(self) -> dict[str, Any]:
        """JWT subject fields."""
        return {"username": self.email}

    @classmethod
    async def by_id(cls, id: str) -> Optional["User"]:
        return await cls.find_one(cls.id == id)

    @classmethod
    async def by_email(cls, email: str) -> Optional["User"]:
        """Get a user by email."""
        return await cls.find_one(cls.email == email)

    def update_email(self, new_email: str) -> None:
        """Update email logging and replace."""
        # Add any pre-checks here
        self.email = new_email

    @classmethod
    async def get_all_users(cls) -> list["User"]:
        return await cls.find().to_list()

    @classmethod
    async def update_member(
        cls, user_id: Optional[str], disable: Optional[str]
    ) -> Optional["User"]:
        """Update user."""
        user = None

        # Find user by ID if provided
        if user_id:
            user = await cls.by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=ResponseCode.not_found.value,
                    detail=ExceptionMessage.user_not_found_by_id.value,
                )
        else:
            raise HTTPException(
                status_code=ResponseCode.bad_request.value,
                detail=ExceptionMessage.user_id_needed.value,
            )

        # Update member status
        if disable.lower() == "true":
            user.disabled = True
        elif disable.lower() == "false":
            user.disabled = False
        else:
            raise HTTPException(
                status_code=ResponseCode.bad_request.value,
                detail=ExceptionMessage.undefined_state_choice.value,
            )

        await user.save()

        return user

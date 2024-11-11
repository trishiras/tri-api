from datetime import timedelta
from pydantic import BaseModel
from tri_api.support.enums import Access


class AccessToken(BaseModel):
    """Access token details."""

    access_token: str
    access_token_expires: timedelta = Access.access_expires.value


class RefreshToken(AccessToken):
    """Access and refresh token details."""

    refresh_token: str
    refresh_token_expires: timedelta = Access.refresh_expires.value

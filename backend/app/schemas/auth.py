from __future__ import annotations

from pydantic import BaseModel

from app.schemas.user import UserResponse


class DemoLoginRequest(BaseModel):
    email: str


class DemoLoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

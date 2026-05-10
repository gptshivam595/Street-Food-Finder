from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.user import UserRole


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    role: UserRole
    created_at: datetime | None = None

    model_config = {"from_attributes": True}

from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=100)
    rating: float = Field(..., ge=1.0, le=5.0)
    hygiene_rating: float = Field(..., ge=1.0, le=5.0)
    comment: str | None = Field(default=None, max_length=1000)


class ReviewResponse(BaseModel):
    id: uuid.UUID
    vendor_id: uuid.UUID
    user_name: str
    rating: float
    hygiene_rating: float
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class ReviewListResponse(BaseModel):
    reviews: list[ReviewResponse]
    total: int
    limit: int
    offset: int

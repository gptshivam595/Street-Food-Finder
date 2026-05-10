from __future__ import annotations

import uuid
from datetime import datetime, time

from pydantic import BaseModel, Field

from app.schemas.food_item import FoodItemResponse


class VendorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    owner_name: str = Field(..., min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    area: str = Field(..., min_length=1, max_length=100)
    address: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    opening_time: time
    closing_time: time
    is_active: bool = True


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    owner_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    area: str | None = Field(default=None, min_length=1, max_length=100)
    address: str | None = Field(default=None, min_length=1)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    opening_time: time | None = None
    closing_time: time | None = None
    is_active: bool | None = None


class VendorInDB(VendorBase):
    id: uuid.UUID
    hygiene_rating: float
    average_rating: float
    review_count: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VendorResponse(VendorInDB):
    is_open_now: bool
    food_items: list[FoodItemResponse] | None = None
    distance_km: float | None = None


class VendorListResponse(BaseModel):
    vendors: list[VendorResponse]
    total: int
    limit: int
    offset: int

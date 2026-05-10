from __future__ import annotations

import uuid

from pydantic import BaseModel


class FoodItemResponse(BaseModel):
    id: uuid.UUID
    vendor_id: uuid.UUID
    name: str
    category: str
    price: float
    is_available: bool

    model_config = {"from_attributes": True}

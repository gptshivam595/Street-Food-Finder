from __future__ import annotations

from datetime import datetime, time, timedelta, timezone

from app.schemas.food_item import FoodItemResponse
from app.schemas.vendor import VendorInDB, VendorResponse


def compute_is_open_now(opening_time: time, closing_time: time) -> bool:
    ist_now = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    current = ist_now.time().replace(tzinfo=None)
    if opening_time <= closing_time:
        return opening_time <= current <= closing_time
    return current >= opening_time or current <= closing_time


def enrich_vendor_response(vendor_orm, include_food_items: bool = False) -> VendorResponse:
    vendor_data = VendorInDB.model_validate(vendor_orm).model_dump()
    food_items = None
    if include_food_items:
        food_items = [FoodItemResponse.model_validate(item) for item in vendor_orm.food_items]
    return VendorResponse(
        **vendor_data,
        is_open_now=compute_is_open_now(vendor_orm.opening_time, vendor_orm.closing_time),
        food_items=food_items,
    )

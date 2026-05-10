from __future__ import annotations

import uuid

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.food_item import FoodItem
from app.models.vendor import Vendor
from app.schemas.vendor import VendorCreate


def get_all(
    db: Session,
    q: str | None = None,
    category: str | None = None,
    open_now: bool | None = None,
    limit: int = 20,
    offset: int = 0,
) -> tuple[list[Vendor], int]:
    query = db.query(Vendor).options(joinedload(Vendor.food_items)).filter(Vendor.is_active.is_(True))
    if q:
        term = f"%{q.strip()}%"
        query = query.outerjoin(FoodItem).filter(
            or_(
                Vendor.name.ilike(term),
                Vendor.description.ilike(term),
                Vendor.area.ilike(term),
                FoodItem.name.ilike(term),
            )
        )
    if category:
        query = query.join(FoodItem).filter(FoodItem.category.ilike(category.strip()))
    vendors = query.distinct().all()
    return vendors, len(vendors)


def get_by_id(db: Session, vendor_id: uuid.UUID | str) -> Vendor | None:
    return (
        db.query(Vendor)
        .options(joinedload(Vendor.food_items))
        .filter(Vendor.id == vendor_id)
        .first()
    )


def create(db: Session, vendor_data: VendorCreate) -> Vendor:
    vendor = Vendor(**vendor_data.model_dump())
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor


def update_ratings(
    db: Session,
    vendor_id: uuid.UUID | str,
    new_avg_rating: float,
    new_avg_hygiene: float,
    new_count: int,
) -> Vendor:
    vendor = get_by_id(db, vendor_id)
    if vendor is None:
        raise ValueError("Vendor not found")
    vendor.average_rating = round(new_avg_rating, 2)
    vendor.hygiene_rating = round(new_avg_hygiene, 2)
    vendor.review_count = new_count
    db.add(vendor)
    db.commit()
    db.refresh(vendor)
    return vendor

from __future__ import annotations

import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.review import Review
from app.schemas.review import ReviewCreate


def get_by_vendor(db: Session, vendor_id: uuid.UUID | str, limit: int = 20, offset: int = 0) -> list[Review]:
    return (
        db.query(Review)
        .filter(Review.vendor_id == vendor_id)
        .order_by(Review.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def get_count_by_vendor(db: Session, vendor_id: uuid.UUID | str) -> int:
    return int(db.query(func.count(Review.id)).filter(Review.vendor_id == vendor_id).scalar() or 0)


def create(db: Session, vendor_id: uuid.UUID | str, review_data: ReviewCreate) -> Review:
    review = Review(vendor_id=vendor_id, **review_data.model_dump())
    db.add(review)
    db.flush()
    db.refresh(review)
    return review


def get_avg_ratings_for_vendor(db: Session, vendor_id: uuid.UUID | str) -> dict[str, float | int]:
    avg_rating, avg_hygiene, count = (
        db.query(
            func.avg(Review.rating),
            func.avg(Review.hygiene_rating),
            func.count(Review.id),
        )
        .filter(Review.vendor_id == vendor_id)
        .one()
    )
    return {
        "avg_rating": float(avg_rating or 0.0),
        "avg_hygiene": float(avg_hygiene or 0.0),
        "count": int(count or 0),
    }

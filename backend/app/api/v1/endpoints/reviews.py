from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories import review_repository, vendor_repository
from app.schemas.review import ReviewCreate, ReviewListResponse, ReviewResponse


router = APIRouter()


@router.get("", response_model=ReviewListResponse)
def list_reviews(
    vendor_id: uuid.UUID,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> ReviewListResponse:
    if vendor_repository.get_by_id(db, vendor_id) is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    reviews = review_repository.get_by_vendor(db, vendor_id, limit, offset)
    total = review_repository.get_count_by_vendor(db, vendor_id)
    return ReviewListResponse(reviews=reviews, total=total, limit=limit, offset=offset)


@router.post("", response_model=ReviewResponse, status_code=201)
def create_review(
    vendor_id: uuid.UUID,
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
) -> ReviewResponse:
    if vendor_repository.get_by_id(db, vendor_id) is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    try:
        review = review_repository.create(db, vendor_id, review_data)
        averages = review_repository.get_avg_ratings_for_vendor(db, vendor_id)
        vendor_repository.update_ratings(
            db,
            vendor_id,
            float(averages["avg_rating"]),
            float(averages["avg_hygiene"]),
            int(averages["count"]),
        )
        db.refresh(review)
        return ReviewResponse.model_validate(review)
    except Exception:
        db.rollback()
        raise

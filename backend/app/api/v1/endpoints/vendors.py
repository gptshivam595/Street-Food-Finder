from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories import vendor_repository
from app.schemas.food_item import FoodItemResponse
from app.schemas.vendor import VendorCreate, VendorListResponse, VendorResponse
from app.services.geo_service import filter_by_radius, sort_vendors_by_distance
from app.services.vendor_service import enrich_vendor_response


router = APIRouter()


@router.get("", response_model=VendorListResponse)
def list_vendors(
    q: str | None = None,
    category: str | None = None,
    lat: float | None = None,
    lng: float | None = None,
    radius_km: float | None = Query(default=None, gt=0),
    open_now: bool | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> VendorListResponse:
    vendors_orm, _ = vendor_repository.get_all(db, q, category, open_now, limit, offset)
    vendors = [enrich_vendor_response(vendor, include_food_items=True) for vendor in vendors_orm]

    if open_now is True:
        vendors = [vendor for vendor in vendors if vendor.is_open_now]

    if lat is not None and lng is not None:
        vendors = sort_vendors_by_distance(vendors, lat, lng)
        if radius_km is not None:
            vendors = filter_by_radius(vendors, lat, lng, radius_km)
            vendors = sorted(vendors, key=lambda vendor: vendor.distance_km if vendor.distance_km is not None else float("inf"))
    else:
        vendors = sorted(vendors, key=lambda vendor: vendor.average_rating, reverse=True)

    total = len(vendors)
    paged = vendors[offset : offset + limit]
    return VendorListResponse(vendors=paged, total=total, limit=limit, offset=offset)


@router.post("", response_model=VendorResponse, status_code=201)
def create_vendor(vendor_data: VendorCreate, db: Session = Depends(get_db)) -> VendorResponse:
    vendor = vendor_repository.create(db, vendor_data)
    return enrich_vendor_response(vendor, include_food_items=True)


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: uuid.UUID, db: Session = Depends(get_db)) -> VendorResponse:
    vendor = vendor_repository.get_by_id(db, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return enrich_vendor_response(vendor, include_food_items=True)


@router.get("/{vendor_id}/food-items", response_model=list[FoodItemResponse])
def get_vendor_food_items(vendor_id: uuid.UUID, db: Session = Depends(get_db)) -> list[FoodItemResponse]:
    vendor = vendor_repository.get_by_id(db, vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return [FoodItemResponse.model_validate(item) for item in vendor.food_items]

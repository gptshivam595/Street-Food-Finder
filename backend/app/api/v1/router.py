from __future__ import annotations

from fastapi import APIRouter

from app.api.v1.endpoints import auth, health, reviews, vendors


api_v1_router = APIRouter()
api_v1_router.include_router(health.router, tags=["health"])
api_v1_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_v1_router.include_router(vendors.router, prefix="/vendors", tags=["vendors"])
api_v1_router.include_router(reviews.router, prefix="/vendors/{vendor_id}/reviews", tags=["reviews"])

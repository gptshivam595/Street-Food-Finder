from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.user_repository import get_or_create_demo_user
from app.schemas.auth import DemoLoginRequest, DemoLoginResponse


router = APIRouter()


@router.post("/demo-login", response_model=DemoLoginResponse)
def demo_login(payload: DemoLoginRequest, db: Session = Depends(get_db)) -> DemoLoginResponse:
    user = get_or_create_demo_user(db, payload.email)
    return DemoLoginResponse(
        access_token="demo-token-not-for-production",
        token_type="bearer",
        user=user,
    )

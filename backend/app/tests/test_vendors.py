from __future__ import annotations

import os
import uuid
from collections.abc import Generator
from datetime import datetime, time, timedelta, timezone

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

os.environ.setdefault("DATABASE_URL", "sqlite+pysqlite:///:memory:")
os.environ.setdefault("FRONTEND_URL", "http://localhost:3000")
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("ENVIRONMENT", "development")

from app.api.deps import get_db
from app.db.base import Base
from app.main import app
from app.models.food_item import FoodItem
from app.models.vendor import Vendor


engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    future=True,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=Session)


def closed_window() -> tuple[time, time]:
    current_ist = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    opening = current_ist + timedelta(hours=1)
    closing = current_ist + timedelta(hours=2)
    return opening.time().replace(microsecond=0, tzinfo=None), closing.time().replace(microsecond=0, tzinfo=None)


def seed_test_vendors(db: Session) -> uuid.UUID:
    open_vendor = Vendor(
        name="Test Open Dosa Cart",
        description="Open all day for tests.",
        owner_name="Test Owner",
        phone="+919999999999",
        area="Indiranagar",
        address="Test Road, Indiranagar",
        latitude=12.9719,
        longitude=77.6412,
        opening_time=time(0, 0, 0),
        closing_time=time(23, 59, 59),
        average_rating=4.0,
        hygiene_rating=4.0,
        review_count=0,
    )
    closed_opening, closed_closing = closed_window()
    closed_vendor = Vendor(
        name="Test Closed Chaat Cart",
        description="Closed during this test run.",
        owner_name="Closed Owner",
        phone=None,
        area="Koramangala",
        address="Test Road, Koramangala",
        latitude=12.9352,
        longitude=77.6245,
        opening_time=closed_opening,
        closing_time=closed_closing,
        average_rating=3.8,
        hygiene_rating=3.9,
        review_count=0,
    )
    db.add_all([open_vendor, closed_vendor])
    db.flush()
    db.add_all(
        [
            FoodItem(vendor_id=open_vendor.id, name="Masala Dosa", category="Dosa", price=80, is_available=True),
            FoodItem(vendor_id=closed_vendor.id, name="Pani Puri", category="Chaat", price=40, is_available=True),
        ]
    )
    db.commit()
    db.refresh(open_vendor)
    return open_vendor.id


@pytest.fixture()
def db_session() -> Generator[tuple[Session, uuid.UUID], None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    vendor_id = seed_test_vendors(db)

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield db, vendor_id
    finally:
        app.dependency_overrides.clear()
        db.close()


@pytest.mark.asyncio
async def test_get_vendors_returns_collection(db_session: tuple[Session, uuid.UUID]) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/vendors")

    assert response.status_code == 200
    payload = response.json()
    assert "vendors" in payload
    assert "total" in payload
    assert payload["total"] == 2


@pytest.mark.asyncio
async def test_get_vendors_open_now_returns_only_open_vendors(db_session: tuple[Session, uuid.UUID]) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/vendors?open_now=true")

    assert response.status_code == 200
    payload = response.json()
    assert payload["vendors"]
    assert all(vendor["is_open_now"] is True for vendor in payload["vendors"])


@pytest.mark.asyncio
async def test_get_vendor_returns_404_for_missing_uuid(db_session: tuple[Session, uuid.UUID]) -> None:
    missing_id = "00000000-0000-0000-0000-000000000000"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get(f"/api/v1/vendors/{missing_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_post_review_creates_review(db_session: tuple[Session, uuid.UUID]) -> None:
    _, vendor_id = db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            f"/api/v1/vendors/{vendor_id}/reviews",
            json={
                "user_name": "Test Reviewer",
                "rating": 4.5,
                "hygiene_rating": 4.0,
                "comment": "Clean and tasty.",
            },
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["user_name"] == "Test Reviewer"
    assert payload["vendor_id"] == str(vendor_id)


@pytest.mark.asyncio
async def test_rating_updates_after_review_submission(db_session: tuple[Session, uuid.UUID]) -> None:
    _, vendor_id = db_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        review_response = await client.post(
            f"/api/v1/vendors/{vendor_id}/reviews",
            json={
                "user_name": "Rating Tester",
                "rating": 5.0,
                "hygiene_rating": 4.5,
                "comment": "Rating aggregate should update.",
            },
        )
        vendor_response = await client.get(f"/api/v1/vendors/{vendor_id}")

    assert review_response.status_code == 201
    assert vendor_response.status_code == 200
    vendor_payload = vendor_response.json()
    assert vendor_payload["average_rating"] == 5.0
    assert vendor_payload["hygiene_rating"] == 4.5
    assert vendor_payload["review_count"] == 1

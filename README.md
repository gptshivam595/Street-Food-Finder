# Street Food Finder

Street Food Finder is a full-stack MVP for discovering Bangalore street food vendors by area, category, live opening status, rating, hygiene score, and map distance.

## Architecture

```text
Browser / Next.js App Router
        |
        | REST JSON
        v
FastAPI API Gateway
        |
        | SQLAlchemy ORM
        v
PostgreSQL

Seed script -> vendors, food items, reviews
Tests       -> FastAPI app with in-memory SQLite
```

## Tech Stack

- Backend: FastAPI, SQLAlchemy 2, Alembic, PostgreSQL, Pydantic v2, Pytest
- Frontend: Next.js 14, React, TypeScript, Tailwind CSS, Axios, Leaflet, React Leaflet
- Local infra: Docker Compose with PostgreSQL 15
- Deployment targets: Railway for backend, Vercel for frontend

## Local Development

```bash
docker-compose up -d
cd backend && cp .env.example .env
alembic upgrade head
python -m app.seed.seed_data
uvicorn app.main:app --reload
cd ../frontend && cp .env.example .env.local
npm install && npm run dev
```

Backend runs on `http://localhost:8000`. Frontend runs on `http://localhost:3000`.

## Railway Deployment

1. Create a Railway project and add a PostgreSQL database.
2. Set the backend root directory to `backend`.
3. Add these variables:
   - `DATABASE_URL`
   - `FRONTEND_URL`
   - `SECRET_KEY`
   - `ENVIRONMENT=production`
   - `PORT`
4. Railway uses `backend/railway.json` to run migrations, seed data, and start Uvicorn.

## Vercel Deployment

1. Import the repository into Vercel.
2. Set the frontend root directory to `frontend`.
3. Add this variable:
   - `NEXT_PUBLIC_API_BASE_URL`
4. Deploy after the Railway backend URL is available.

## API Contract

`GET /api/v1/health`

Response:

```json
{"status": "ok", "version": "1.0.0", "environment": "development"}
```

`GET /api/v1/vendors`

Query: `q`, `category`, `lat`, `lng`, `radius_km`, `open_now`, `limit`, `offset`

Response:

```json
{
  "vendors": [
    {
      "id": "uuid",
      "name": "Vendor name",
      "area": "Indiranagar",
      "opening_time": "08:00:00",
      "closing_time": "22:00:00",
      "average_rating": 4.5,
      "hygiene_rating": 4.4,
      "review_count": 12,
      "is_open_now": true,
      "distance_km": 1.2,
      "food_items": []
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

`GET /api/v1/vendors/{vendor_id}`

Response: one vendor with `food_items`.

`GET /api/v1/vendors/{vendor_id}/food-items`

Response: list of food items.

`GET /api/v1/vendors/{vendor_id}/reviews`

Response:

```json
{"reviews": [], "total": 0, "limit": 20, "offset": 0}
```

`POST /api/v1/vendors/{vendor_id}/reviews`

Request:

```json
{"user_name": "Demo User", "rating": 5, "hygiene_rating": 5, "comment": "Excellent"}
```

Response: created review. The vendor average rating, hygiene rating, and review count are recalculated from all reviews.

`POST /api/v1/vendors`

Request: vendor create payload without computed fields.

Response: created vendor with `is_open_now`.

`POST /api/v1/auth/demo-login`

Request:

```json
{"email": "demo@streetfood.app"}
```

Response:

```json
{
  "access_token": "demo-token-not-for-production",
  "token_type": "bearer",
  "user": {"id": "uuid", "name": "Demo User", "email": "demo@streetfood.app", "role": "CUSTOMER"}
}
```

## MVP Scope

- Discover seeded Bangalore street food vendors.
- Search vendors by text and filter by category or open status.
- Sort vendors by rating or distance when location is available.
- View vendor details, menu items, ratings, reviews, and map location.
- Submit reviews and update rating aggregates.
- Deploy backend and frontend independently.

## Future Improvements

- Vendor owner authentication and dashboard.
- Photo uploads for stalls and dishes.
- Moderation workflow for reviews.
- Saved favorites and personalized recommendations.
- Real-time vendor status updates.
- Production Alembic revision history after schema stabilizes.

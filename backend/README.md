# Street Food Finder Backend

FastAPI backend for vendors, food items, reviews, demo login, health checks, seed data, and deployment on Railway.

## Setup

```bash
python -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python -m app.seed.seed_data
uvicorn app.main:app --reload
```

## Environment

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/streetfood
FRONTEND_URL=http://localhost:3000
SECRET_KEY=your-secret-key-here-change-in-production
ENVIRONMENT=development
PORT=8000
```

## Testing

```bash
pytest app/tests
```

The tests override the FastAPI database dependency with an in-memory SQLite engine.

## Deployment

Railway uses `railway.json` and `Procfile`. The start command runs Alembic, seeds missing vendors idempotently, then starts Uvicorn.

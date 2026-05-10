# Street Food Finder Backend

FastAPI backend for vendors, food items, reviews, demo login, health checks, seed data, and deployment on Render.

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

## Render Deployment

Use the repository-root `render.yaml` blueprint, or create a manual Render Web Service with:

```bash
pip install -r requirements.txt
```

Start command:

```bash
python -m app.seed.seed_data && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Required Render environment variables:

```env
DATABASE_URL=<Render PostgreSQL connection string>
FRONTEND_URL=https://your-vercel-app.vercel.app
SECRET_KEY=<generated-secret>
ENVIRONMENT=production
PYTHON_VERSION=3.11.9
```

The seed command is idempotent, so redeploys do not duplicate vendors.

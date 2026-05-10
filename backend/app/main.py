from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.cors import setup_cors
from app.db.init_db import init_db


app = FastAPI(
    title="Street Food Finder API",
    version="1.0.0",
    description="API for discovering Bangalore street food vendors, menus, timings, hygiene ratings, and reviews.",
)

setup_cors(app, settings)
app.include_router(api_v1_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.PORT, reload=settings.ENVIRONMENT == "development")

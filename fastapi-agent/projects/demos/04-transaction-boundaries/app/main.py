from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api.users import router as users_router
from app.db import reset_database


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await reset_database()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "healthy"}

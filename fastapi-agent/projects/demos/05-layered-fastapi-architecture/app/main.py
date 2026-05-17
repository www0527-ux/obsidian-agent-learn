from __future__ import annotations

from fastapi import FastAPI

from app.api.routes.users import router as users_router


def create_app() -> FastAPI:
    app = FastAPI(title="Layered FastAPI Practice")

    # TODO: include users_router.
    # TODO: optionally register global exception handlers here.
    app.router.include_router(users_router)
    return app
app = create_app()



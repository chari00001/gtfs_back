from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app import __version__
from app.api.router import api_router
from app.core.config import get_settings
from app.core.logging_config import configure_logging
from app.db.database import engine
from app.models.base import Base
from app.models import *  # noqa: F401,F403 - ensure all models are imported for Base.metadata

@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.DEBUG)
    logging.getLogger(__name__).info("Starting app v%s", __version__)

    # Database connection check and logging
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logging.getLogger(__name__).info(
            "Database connected: %s | Pool: %s",
            engine.url.render_as_string(hide_password=True),
            getattr(engine.pool, "status", lambda: "unknown")(),
        )
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        logging.getLogger(__name__).warning("DB init skipped: %s", exc)

    try:
        yield
    finally:
        logging.getLogger(__name__).info("Disposing database engine")
        engine.dispose()

 


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=__version__,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.BACKEND_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()



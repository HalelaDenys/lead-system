from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager
from infrastructure import db_helper, broker, redis_client
import logging
from shared import settings
from landing_service.api import main_router
from landing_service.core import middlewares, error_handlers

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("broker starting ...")
    await broker.start()
    await redis_client.connect()

    yield

    await db_helper.dispose()

    await redis_client.close()
    await broker.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
    )

    error_handlers.register_error_handlers(app)
    middlewares.register_middleware(app)

    app.include_router(main_router)

    return app

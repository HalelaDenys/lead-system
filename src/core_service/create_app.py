from core_service.core import error_handlers, middlewares
from core_service.schemas import main_router
from infrastructure import db_helper, redis_client
from core_service.container import init_container
from core_service.broker.consumer import broker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from shared import settings
from fastapi import FastAPI
import logging

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.info("starting core service")

    await redis_client.connect()

    await init_container()

    await broker.start()

    yield

    await broker.stop()
    await redis_client.close()
    await db_helper.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title="Core Service",
    )

    error_handlers.register_error_handlers(app)
    middlewares.register_middleware(app)

    app.include_router(main_router)

    return app

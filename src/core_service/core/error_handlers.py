from faststream.exceptions import FastStreamException
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DatabaseError
from shared.exceptions import (
    NotFoundError,
    AlreadyExistsError,
    UnauthorizedException,
    TokenExpiredException,
    InvalidTokenException,
)
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:

    @app.exception_handler(NotFoundError)
    async def not_found(request: Request, exc: NotFoundError) -> JSONResponse:
        logger.warning("Not found: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AlreadyExistsError)
    async def already_exists(request: Request, exc: AlreadyExistsError) -> JSONResponse:
        logger.warning("Already exists: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UnauthorizedException)
    async def unauthorized(
        request: Request, exc: UnauthorizedException
    ) -> JSONResponse:
        logger.warning("Unauthorized: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(TokenExpiredException)
    async def token_expired_exists(
        request: Request, exc: TokenExpiredException
    ) -> JSONResponse:
        logger.warning("Token expired: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": str(exc)},
        )

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_exists(
        request: Request, exc: InvalidTokenException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc),
            },
        )

    @app.exception_handler(DatabaseError)
    async def database_error(request: Request, exc: DatabaseError):
        logger.exception("Database error: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )

    @app.exception_handler(ConnectionRefusedError)
    async def connection_error(request: Request, exc: ConnectionRefusedError):
        logger.exception("Connection refused: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Service unavailable"},
        )

    @app.exception_handler(FastStreamException)
    async def faststream_error(request: Request, exc: FastStreamException):
        logger.exception("FastStream error: %s", str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Service unavailable"},
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled error: %s", str(exc))
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"},
        )

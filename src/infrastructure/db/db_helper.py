from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
    AsyncSession,
)
from typing import AsyncGenerator
from sqlalchemy.engine import URL
from shared.config import settings


class DBHelper:
    def __init__(
        self,
        *,
        url: str | URL,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 5,
        max_overflow: int = 10,
    ):
        self._engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            echo_pool=echo_pool,
        )

        self._async_session_maker: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self._engine,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self._async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def dispose(self) -> None:
        await self._engine.dispose()


db_helper = DBHelper(
    url=settings.db.dsn,
    echo=settings.db.alchemy_config.echo,
    echo_pool=settings.db.alchemy_config.echo_pool,
    pool_size=settings.db.alchemy_config.pool_size,
    max_overflow=settings.db.alchemy_config.max_overflow,
)

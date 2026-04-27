from redis.asyncio import Redis
from shared.config import settings
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self, url: str):
        self.url = url
        self._redis: Redis | None = None

    async def connect(self) -> None:
        if self._redis is None:
            self._redis = Redis.from_url(
                self.url,
                encoding="utf-8",
                decode_responses=True,
            )
            try:
                await self._redis.ping()
                logger.info("Successfully connected Redis")
            except Exception as e:
                self._redis = None
                logger.error("Failed to connect to Redis: %s", e)
                raise

    async def close(self) -> None:
        if self._redis:
            await self._redis.aclose()
            self._redis = None
            logger.info("Closing Redis")

    def get_client(self) -> Redis:
        if self._redis is None:
            raise RuntimeError("Redis client not connected")
        return self._redis


redis_client = RedisClient(
    url=settings.redis.dsn,
)

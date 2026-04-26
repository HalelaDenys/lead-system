from redis.asyncio import Redis
from shared.config import settings


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

    async def close(self) -> None:
        if self._redis:
            await self._redis.aclose()
            self._redis = None

    def get_client(self) -> Redis:
        if self._redis is None:
            raise RuntimeError("Redis client not connected")
        return self._redis


redis_client = RedisClient(
    url=settings.redis.dsn,
)

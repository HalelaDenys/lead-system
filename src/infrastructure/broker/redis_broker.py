from faststream.redis import RedisBroker
from shared.config import settings

broker = RedisBroker(
    url=settings.redis.dsn,
)

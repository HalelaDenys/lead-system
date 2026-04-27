from core_service.service.lead_dedup_service import LeadDedupService
from infrastructure.redis.client import redis_client


class Container:
    dedup: LeadDedupService | None = None


container = Container()


async def init_container():
    container.dedup = LeadDedupService(
        redis=redis_client.get_client(),
    )

from core_service.dto.lead_dto import LeadDataKeyDTO
import hashlib

from redis.asyncio import Redis


class LeadDedupService:
    def __init__(self, redis: Redis, ttl_seconds: int = 600):
        self.redis = redis
        self.ttl_seconds = ttl_seconds

    async def mark_if_not_exists(self, lead_data_key: LeadDataKeyDTO) -> bool:
        key = self._build_key(lead_data_key)

        return await self.redis.set(
            key,
            "1",
            ex=self.ttl_seconds,
            nx=True,
        )

    def _build_key(self, lead_data_key: LeadDataKeyDTO) -> str:
        raw = f"{lead_data_key.name}:{lead_data_key.phone}:{lead_data_key.offer_id}:{lead_data_key.affiliate_id}"
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        return f"lead:dedupe:{hashed}"

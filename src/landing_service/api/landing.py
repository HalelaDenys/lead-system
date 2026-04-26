from uuid import UUID

from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated

from redis.asyncio import Redis

from infrastructure import redis_client
from shared.security.auth import get_current_affiliate_deps

api_router = APIRouter(tags=["Landing"], prefix="/api/v1/landing")


@api_router.post("", status_code=201)
async def submit_lead(
    led: str, affiliate_id: Annotated[UUID, Depends(get_current_affiliate_deps)]
):
    return {"id": str(affiliate_id)}

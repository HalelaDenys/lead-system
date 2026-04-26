from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from shared import Security, SubTokenPayloadDTO
from fastapi import HTTPException, Depends
from infrastructure import redis_client
from redis.asyncio import Redis
from typing import Annotated
from uuid import UUID

http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> dict:

    if credentials is None:
        raise HTTPException(status_code=401, detail="Missing auth header")

    token = credentials.credentials

    try:
        return Security.decode_token(token=str(token))
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_token_data_and_validate(
    payload: Annotated[dict, Depends(get_current_token_payload)],
) -> SubTokenPayloadDTO:

    Security.validate_exp(payload)
    return Security.extract_sub(payload)


async def get_current_affiliate_deps(
    token_data: Annotated[SubTokenPayloadDTO, Depends(get_token_data_and_validate)],
    redis: Annotated[Redis, Depends(redis_client.get_client)],
) -> SubTokenPayloadDTO:

    affiliate_id = await redis.get(f"active_affiliate:{token_data.sub}")

    if not affiliate_id:
        raise HTTPException(
            status_code=401,
            detail="Affiliate not found",
        )

    return SubTokenPayloadDTO(sub=UUID(affiliate_id))

from landing_service.schemas.landing_schema import CreateLeadSchema
from landing_service.broker.publisher import LeadPublisher
from fastapi import Depends, APIRouter, HTTPException
from typing import Annotated
from shared import settings
from uuid import UUID
import logging

from shared.security.auth import get_current_affiliate_id

api_router = APIRouter(prefix=settings.prefix.landings)

logger = logging.getLogger(__name__)


@api_router.post(
    "/lead",
    status_code=200,
    summary="Submit a lead from a landing page.",
    description="Accepts a lead payload, validates all fields, verifies that the "
    "affiliate_id in the body matches the one encoded in the Bearer token, "
    "and pushes the lead to the Redis processing queue.",
    responses={
        200: {"description": "Lead accepted and queued for processing"},
        401: {"description": "Invalid token or affiliate not found"},
        403: {"description": "affiliate_id in body does not match token"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal Error"},
    },
)
async def submit_lead(
    lead_data: CreateLeadSchema,
    affiliate_id: Annotated[UUID, Depends(get_current_affiliate_id)],
) -> dict:
    if UUID(str(lead_data.affiliate_id)) != affiliate_id:
        logger.warning(
            "affiliate_id mismatch: affiliate_id from the token=%s, body=%s",
            affiliate_id,
            lead_data.affiliate_id,
        )
        raise HTTPException(
            status_code=403,
            detail="Invalid affiliate ID",
        )

    await LeadPublisher.lead_publish_message(lead_data=lead_data)
    return {"status": "accepted"}

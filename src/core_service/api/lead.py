from uuid import UUID

from fastapi import APIRouter, Depends, Query
from typing import Annotated

from core_service.dto.lead_dto import LeadDataByPeriodDTO
from core_service.schemas.lead_schema import LeadQueryParams
from core_service.service.lead_service import LeadService, get_lead_service
from shared.security.auth import get_current_affiliate_id
from shared import settings

api_router = APIRouter(prefix=settings.prefix.core)


@api_router.get(
    "/leads",
    summary="Get affiliate lead analytics",
    description=(
        "Returns an aggregated summary of leads belonging to the authenticated affiliate "
        "for the given date range. Use `group=date` to group by day, or `group=offer` "
        "to group by offer."
    ),
    responses={
        200: {"description": "Aggregated lead summary"},
        400: {"description": "date_from must be <= date_to"},
        401: {"description": "Invalid/missing token or affiliate not found"},
        422: {"description": "Validation error"},
    },
)
async def get_leads(
    q_params: Annotated[LeadQueryParams, Query()],
    lead_service: Annotated["LeadService", Depends(get_lead_service)],
    affiliate_id: Annotated[UUID, Depends(get_current_affiliate_id)],
):
    return await lead_service.get_leads(
        lead_data=LeadDataByPeriodDTO(
            affiliate_id=affiliate_id,
            date_to=q_params.date_to,
            date_from=q_params.date_from,
        ),
        group=q_params.group,
    )

from landing_service.api.lead import api_router
from fastapi import APIRouter
from shared import settings

main_router = APIRouter(tags=["Landing service"], prefix=settings.prefix.api_v1)
main_router.include_router(api_router)

from fastapi import APIRouter
from core_service.api.lead import api_router

main_router = APIRouter(tags=["Core Service"])
main_router.include_router(api_router)

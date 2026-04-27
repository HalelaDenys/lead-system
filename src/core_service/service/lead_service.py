from core_service.schemas.lead_schema import GroupByDateResponse, GroupByOfferResponse
from core_service.dto.lead_dto import CreateLeadDTO, LeadDataByPeriodDTO
from core_service.repo.lead_repo import LeadRepo
from infrastructure import db_helper
from typing import AsyncGenerator


class LeadService:
    def __init__(self, user_repo: LeadRepo):
        self._lead_repo = user_repo

    async def add_lead(self, lead_data: CreateLeadDTO):
        await self._lead_repo.create(data=lead_data)

    async def get_leads(self, lead_data: LeadDataByPeriodDTO, group: str):
        if group == "date":
            res = await self._lead_repo.get_grouped_by_date(
                lead_data=lead_data,
            )

            return [GroupByDateResponse(date=r.date, count=r.count) for r in res]

        if group == "offer":
            res = await self._lead_repo.get_grouped_by_offer(
                lead_data=lead_data,
            )
            return [
                GroupByOfferResponse(offer_id=r.offer_id, count=r.count) for r in res
            ]

        raise ValueError("Invalid group")


async def get_lead_service() -> AsyncGenerator[LeadService, None]:
    async with db_helper.get_session() as session:
        affiliate_repo = LeadRepo(session)
        yield LeadService(affiliate_repo)

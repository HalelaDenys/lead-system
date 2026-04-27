from typing import Sequence

from core_service.dto.lead_dto import LeadDataByPeriodDTO
from infrastructure import BaseSqlalchemyRepo, Lead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


class LeadRepo(BaseSqlalchemyRepo[Lead]):
    def __init__(self, session: AsyncSession):
        super().__init__(Lead, session)

    async def get_grouped_by_date(self, lead_data: LeadDataByPeriodDTO):
        stmt = (
            select(
                func.date(self._model.created_at).label("date"),
                func.count(self._model.created_at).label("count"),
            )
            .where(
                self._model.affiliate_id == lead_data.affiliate_id,
                self._model.created_at >= lead_data.date_from,
                self._model.created_at <= lead_data.date_to,
            )
            .group_by(func.date(self._model.created_at))
            .order_by(func.date(self._model.created_at))
        )

        res = await self._session.execute(stmt)
        return res.all()

    async def get_grouped_by_offer(self, lead_data: LeadDataByPeriodDTO):
        stmt = (
            select(
                self._model.offer_id.label("offer_id"),
                func.count(self._model.id).label("count"),
            )
            .where(
                self._model.affiliate_id == lead_data.affiliate_id,
                self._model.created_at >= lead_data.date_from,
                self._model.created_at <= lead_data.date_to,
            )
            .group_by(self._model.offer_id)
        )

        res = await self._session.execute(stmt)
        return res.all()

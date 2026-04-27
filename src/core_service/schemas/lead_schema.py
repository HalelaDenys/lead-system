from datetime import date
from typing import Literal
from uuid import UUID
from shared import BaseSchema


class LeadQueueMessage(BaseSchema):
    name: str
    phone: str
    country: str
    offer_id: UUID
    affiliate_id: UUID


class LeadQueryParams(BaseSchema):
    date_from: date
    date_to: date
    group: Literal["date", "offer"] = ("date",)


class LeadItem(BaseSchema):
    id: UUID
    name: str
    phone: str
    offer_id: UUID
    created_at: date


class GroupByDateResponse(BaseSchema):
    date: date
    count: int


class GroupByOfferResponse(BaseSchema):
    offer_id: UUID
    count: int

from dataclasses import dataclass
from datetime import date
from uuid import UUID


@dataclass(frozen=True, slots=True)
class LeadDataKeyDTO:
    name: str
    phone: str
    offer_id: str
    affiliate_id: str


@dataclass(frozen=True, slots=True)
class CreateLeadDTO:
    name: str
    phone: str
    country: str
    offer_id: UUID
    affiliate_id: UUID


@dataclass(frozen=True, slots=True)
class LeadDataByPeriodDTO:
    affiliate_id: UUID
    date_from: date
    date_to: date

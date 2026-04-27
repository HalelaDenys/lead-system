from uuid import UUID

from shared import BaseSchema
from typing import Annotated
from pydantic import Field, field_validator
import re


class CreateLeadSchema(BaseSchema):
    name: Annotated[str, Field(min_length=3, max_length=255, description="Lead name")]
    phone: str
    country: Annotated[
        str,
        Field(
            min_length=2,
            max_length=2,
            description="country must be ISO 3166-1 alpha-2 (e.g. UA)",
        ),
    ]
    offer_id: Annotated[UUID, Field(description="Offer ID")]
    affiliate_id: Annotated[UUID, Field(description="Affiliate ID")]

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()

        if v.startswith("+"):
            digits = "+" + re.sub(r"\D", "", v)
        else:
            digits = re.sub(r"\D", "", v)

        if not (9 <= len(digits.replace("+", "")) <= 15):
            raise ValueError("Invalid phone length")

        return digits

    @field_validator("country")
    @classmethod
    def validate_country(cls, v: str) -> str:
        v = v.upper()
        if not v.isalpha():
            raise ValueError("Invalid country code")
        return v


class LeadQueueMessage(BaseSchema):
    """Message pushed to Redis steams queue."""

    name: str
    phone: str
    country: str
    offer_id: UUID
    affiliate_id: UUID

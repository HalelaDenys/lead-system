from infrastructure import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import VARCHAR, ForeignKey, Index
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure import Affiliate, Offer


class Lead(Base):
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    phone: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    country: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)

    offer_id: Mapped[int] = mapped_column(
        ForeignKey("offers.id"),
        nullable=False,
    )
    affiliate_id: Mapped[int] = mapped_column(
        ForeignKey("affiliates.id"), nullable=False
    )

    __table_args__ = (
        Index("idx_leads_affiliate_created", "affiliate_id", "created_at"),
        Index("idx_leads_offer_created", "offer_id", "created_at"),
    )

    offer: Mapped["Offer"] = relationship("Offer", back_populates="leads")
    affiliate: Mapped["Affiliate"] = relationship("Affiliate", back_populates="leads")

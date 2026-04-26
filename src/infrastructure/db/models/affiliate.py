from infrastructure import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import VARCHAR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from infrastructure import Lead


class Affiliate(Base):
    name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    leads: Mapped[list["Lead"]] = relationship("Lead", back_populates="affiliate")

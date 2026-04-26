import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import UUID, func, TIMESTAMP, MetaData
from datetime import datetime

from shared.config import settings


class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    def to_dict(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

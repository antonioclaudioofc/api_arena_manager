from app.core.database import Base

from sqlalchemy import UUID, Column, String, ForeignKey, Time
from sqlalchemy.orm import relationship

from app.shared.models.base import ActiveMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Arena(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, ActiveMixin):
    __tablename__ = "arenas"

    name = Column(String)
    slug = Column(String, unique=True)
    description = Column(String, nullable=True)

    phone = Column(String)
    email = Column(String, nullable=True)

    address = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)

    opening_time = Column(Time, nullable=True)
    closing_time = Column(Time, nullable=True)

    owner_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    owner = relationship("User", back_populates="arenas")

    courts = relationship(
        "Court",
        back_populates="arena",
        cascade="all, delete"
    )

    reservations = relationship(
        "Reservation",
        back_populates="arena"
    )

    matches = relationship(
        "Match",
        back_populates="arena"
    )

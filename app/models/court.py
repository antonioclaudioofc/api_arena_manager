from app.core.database import Base

from sqlalchemy import UUID, Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.shared.models.base import ActiveMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin


class Court(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, ActiveMixin):
    __tablename__ = "courts"

    name = Column(String)
    slug = Column(String, unique=True)
    sport_type = Column(String)
    surface_type = Column(String, default="SAND")

    price_per_hour = Column(Float)

    arena_id = Column(UUID(as_uuid=True), ForeignKey("arenas.id"), index=True)

    arena = relationship("Arena", back_populates="courts")

    reservations = relationship(
        "Reservation",
        back_populates="court"
    )

    matches = relationship(
        "Match",
        back_populates="court"
    )

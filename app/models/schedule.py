from app.core.database import Base

from sqlalchemy import UUID, Column, String, Numeric, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.shared.models.base import TimestampMixin, UUIDMixin


class Schedule(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "schedules"

    arena_id = Column(
        UUID(as_uuid=True),
        ForeignKey("arenas.id"),
        index=True
    )

    court_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courts.id"),
        index=True
    )

    date = Column(String, index=True)
    start_time = Column(String, index=True)
    end_time = Column(String)

    price = Column(Numeric(10, 2))

    arena = relationship("Arena", back_populates="schedules")
    court = relationship("Court", back_populates="schedules")
    reservation = relationship(
        "Reservation", back_populates="schedule", uselist=False
    )

    __table_args__ = (
        UniqueConstraint(
            "court_id",
            "date",
            "start_time",
            "end_time",
            name="uq_court_schedule_range"
        ),
    )

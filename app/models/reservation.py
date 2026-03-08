from app.core.database import Base

from sqlalchemy import UUID, Column, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.shared.enums.reservation import ReservationStatus
from app.shared.models.base import TimestampMixin, UUIDMixin


class Reservation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "reservations"

    schedule_id = Column(
        UUID(as_uuid=True),
        ForeignKey("schedules.id"),
        unique=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    status = Column(
        Enum(ReservationStatus, name="reservation_status_enum"),
        default=ReservationStatus.PENDING,
    )

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

    arena = relationship("Arena", back_populates="reservations")
    court = relationship("Court", back_populates="reservations")
    schedule = relationship("Schedule", back_populates="reservation")
    user = relationship("User", back_populates="reservations")
    payments = relationship("Payment", back_populates="reservation")

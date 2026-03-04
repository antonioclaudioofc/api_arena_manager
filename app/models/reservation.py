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

    schedule = relationship("Schedule", back_populates="reservation")
    user = relationship("User", back_populates="reservations")
    payments = relationship("Payment", back_populates="reservation")

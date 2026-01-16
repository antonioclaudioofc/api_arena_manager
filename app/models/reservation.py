from sqlalchemy import Column, DateTime, Enum, Integer, String, ForeignKey
from app.core.database import Base
from sqlalchemy.orm import relationship

from app.shared.enums import ReservationStatus


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(
        Integer,
        ForeignKey(
            "schedules.id", ondelete="CASCADE"
        )
    )
    client_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(Enum(ReservationStatus), default=ReservationStatus.active)
    cancelled_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    schedule = relationship(
        "Schedules",
        back_populates="reservations"
    )
    client = relationship(
        "Users",
        back_populates="reservations"
    )

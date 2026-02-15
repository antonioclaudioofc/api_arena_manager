from app.core.database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship


class Schedule(Base):
    __tablename__ = "schedules"

    __table_args__ = (
        UniqueConstraint(
            "court_id",
            "date",
            "start_time",
            "end_time",
            name="uq_court_schedule"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    court_id = Column(Integer, ForeignKey("courts.id", ondelete="CASCADE"))
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    court = relationship(
        "Court",
        back_populates="schedules"
    )
    reservations = relationship(
        "Reservation",
        back_populates="schedule",
        cascade="all, delete"
    )

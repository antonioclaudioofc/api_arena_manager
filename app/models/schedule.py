from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship


class Schedules(Base):
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
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    available = Column(Boolean)

    court_id = Column(
        Integer,
        ForeignKey("courts.id")
    )
    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(String)
    updated_at = Column(String)

    court = relationship("Courts", back_populates="schedules")
    reservations = relationship(
        "Reservations",
        back_populates="schedule",
        cascade="all, delete-orphan"
    )

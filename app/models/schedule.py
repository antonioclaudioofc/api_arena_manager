from app.core.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship


class Schedules(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    available = Column(Boolean)

    court_id = Column(
        Integer,
        ForeignKey("courts.id", ondelete="CASCADE")
    )

    created_at = Column(String)
    updated_at = Column(String)

    court = relationship("Courts", back_populates="schedules")

    reservations = relationship(
        "Reservations",
        back_populates="schedule",
        cascade="all, delete-orphan"
    )

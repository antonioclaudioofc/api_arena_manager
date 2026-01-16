from app.core.database import Base
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, ForeignKey
from sqlalchemy.orm import relationship


class Court(Base):
    __tablename__ = "courts"

    id = Column(Integer, primary_key=True, index=True)
    arena_id = Column(Integer, ForeignKey("arenas.id", ondelete="CASCADE"))
    name = Column(String)
    sport_type = Column(String)
    price_per_hour = Column(Numeric)
    description = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    arena = relationship(
        "Arena",
        back_populates="courts"
    )
    schedules = relationship(
        "Schedule",
        back_populates="court",
        cascade="all, delete"
    )

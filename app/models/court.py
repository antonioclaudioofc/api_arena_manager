from app.core.database import Base
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Courts(Base):
    __tablename__ = "courts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    sports_type = Column(String)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)

    created_at = Column(String)
    updated_at = Column(String)

    schedules = relationship(
        "Schedules",
        back_populates="court",
        cascade="all, delete-orphan"
    )

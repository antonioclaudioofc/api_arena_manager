from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.core.database import Base
from sqlalchemy.orm import relationship


class Arena(Base):
    __tablename__ = "arenas"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String)
    city = Column(String)
    address = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    owner = relationship(
        "User",
        back_populates="arenas"
    )
    courts = relationship(
        "Court",
        back_populates="arena",
        cascade="all, delete"
    )

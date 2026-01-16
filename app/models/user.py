from app.core.database import Base
from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.shared.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(
        Enum(UserRole, name="user_role"),
        default=UserRole.client
    )
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    arenas = relationship(
        "Arena",
        back_populates="owner",
        cascade="all, delete"
    )
    reservations = relationship(
        "Reservation",
        back_populates="client",
        cascade="all, delete"
    )

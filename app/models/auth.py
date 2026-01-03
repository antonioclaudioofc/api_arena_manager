from app.core.database import Base
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship

from app.shared.enums import UserRole


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    role = Column(
        Enum(UserRole, name="user_role"),
        default=UserRole.client
    )

    created_at = Column(String)
    updated_at = Column(String)

    reservations = relationship(
        "Reservations",
        back_populates="user",
        cascade="all, delete-orphan"
    )

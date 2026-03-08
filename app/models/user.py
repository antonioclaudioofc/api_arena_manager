from app.core.database import Base

from sqlalchemy import Column, Enum, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.shared.enums.user import UserRole
from app.shared.models.base import ActiveMixin, SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin, ActiveMixin):
    __tablename__ = "users"

    name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

    is_email_verified = Column(Boolean, default=False)
    email_verification_token = Column(String, nullable=True)
    reset_password_token = Column(String, nullable=True)
    reset_password_token_expires_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    role = Column(
        Enum(UserRole, name="user_role")
    )

    arenas = relationship(
        "Arena",
        back_populates="owner",
        cascade="all, delete"
    )

    reservations = relationship(
        "Reservation",
        back_populates="user",
        cascade="all, delete"
    )

    matches_created = relationship(
        "Match",
        back_populates="creator"
    )

    payments = relationship(
        "Payment",
        back_populates="user"
    )

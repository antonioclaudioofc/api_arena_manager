from app.core.database import Base

from sqlalchemy import UUID, Column, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from app.shared.models.base import TimestampMixin, UUIDMixin


class MatchParticipant(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "match_participants"

    match_id = Column(
        UUID(as_uuid=True),
        ForeignKey("matches.id"),
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )
    is_confirmed = Column(Boolean, default=True)

    match = relationship("Match", back_populates="participants")

    __table_args__ = (
        UniqueConstraint(
            "match_id",
            "user_id",
            name="uq_match_user"
        ),
    )

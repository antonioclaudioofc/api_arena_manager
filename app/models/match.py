from app.core.database import Base

from sqlalchemy import UUID, Column, DateTime, Integer, ForeignKey, Enum, String
from sqlalchemy.orm import relationship

from app.shared.enums.match import MatchStatus, MatchVisibility, SkillLevel
from app.shared.models.base import SoftDeleteMixin, TimestampMixin, UUIDMixin


class Match(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "matches"

    title = Column(String(150), nullable=False)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    description = Column(String)

    level = Column(
        Enum(SkillLevel, name="skill_level_enum"),
        default=SkillLevel.BEGINNER,
        nullable=False
    )

    visibility = Column(
        Enum(MatchVisibility, name="match_visibility_enum"),
        default=MatchVisibility.PUBLIC,
        nullable=False
    )

    status = Column(
        Enum(MatchStatus, name="match_status_enum"),
        default=MatchStatus.SCHEDULED,
        nullable=False
    )

    start_time = Column(DateTime(timezone=True), index=True)
    end_time = Column(DateTime(timezone=True))

    max_players = Column(Integer, default=16)

    arena_id = Column(
        UUID(as_uuid=True),
        ForeignKey("arenas.id"),
        index=True
    )
    court_id = Column(
        UUID(as_uuid=True),
        ForeignKey("courts.id"),
        index=True
    )
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    arena = relationship("Arena", back_populates="matches")
    court = relationship("Court", back_populates="matches")
    creator = relationship("User", back_populates="matches_created")

    participants = relationship(
        "MatchParticipant",
        back_populates="match",
        cascade="all, delete-orphan"
    )

from app.core.database import Base

from sqlalchemy import UUID, Column, ForeignKey, Enum, DateTime, Numeric, String
from sqlalchemy.orm import relationship

from app.shared.enums.payment import PaymentMethod, PaymentStatus
from app.shared.models.base import TimestampMixin, UUIDMixin


class Payment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payments"

    amount = Column(Numeric(10, 2))

    method = Column(
        Enum(PaymentMethod, name="payment_method_enum")
    )

    status = Column(
        Enum(PaymentStatus, name="payment_status_enum"),
        default=PaymentStatus.PENDING
    )

    external_id = Column(String, nullable=True)
    paid_at = Column(DateTime(timezone=True), nullable=True)

    reservation_id = Column(
        UUID(as_uuid=True),
        ForeignKey("reservations.id"),
        index=True
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        index=True
    )

    reservation = relationship("Reservation", back_populates="payments")
    user = relationship("User", back_populates="payments")

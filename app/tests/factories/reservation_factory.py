from datetime import datetime, timezone
from app.models.reservation import Reservation
from app.shared.enums import ReservationStatus


def reservation_factory(
    db,
    client_id: int,
    schedule_id: int,
    status=ReservationStatus.active,
    cancelled_at=None
):
    reservation = Reservation(
        client_id=client_id,
        schedule_id=schedule_id,
        status=status,
        cancelled_at=cancelled_at,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation

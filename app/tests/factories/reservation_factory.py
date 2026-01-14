from datetime import datetime, timezone

from app.models.reservation import Reservations


def reservation_factory(
    db,
    *,
    user_id: int,
    schedule_id: int,
):
    reservation = Reservations(
        user_id=user_id,
        schedule_id=schedule_id,
        status="Ocupado",
        created_at=datetime.now(timezone.utc)
    )

    db.commit(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation

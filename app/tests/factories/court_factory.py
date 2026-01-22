from datetime import datetime, timezone
from app.models.court import Court


def court_factory(
    db,
    arena_id,
    name="Quadra A",
    sports_type="Vôleiball",
    price_per_hour=99.99
):
    court = Court(
        arena_id=arena_id,
        name=name,
        sports_type=sports_type,
        price_per_hour=price_per_hour,
        created_at=datetime.now(timezone.utc)
    )

    db.add(court)
    db.commit()
    db.refresh(court)

    return court

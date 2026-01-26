from datetime import datetime, timezone
from app.models.arena import Arena


def arena_factory(
    db,
    owner_id: int,
    name="Arena A",
    city="Maranhão",
    address="Rua 4"
):
    arena = Arena(
        name=name,
        city=city,
        address=address,
        owner_id=owner_id,
        created_at=datetime.now(timezone.utc)
    )

    db.add(arena)
    db.commit()
    db.refresh(arena)

    return arena

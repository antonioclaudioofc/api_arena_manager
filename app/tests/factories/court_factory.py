from datetime import datetime, timezone
from app.dependencies import db_dependency
from app.models.court import Courts


def court_factory(
    db: db_dependency,
    *,
    name: str = "Quadra A",
    sports_type: str = "Vôlei",
    description: str = "Quadra coberta",
    created_at=datetime.now(timezone.utc),
    updated_at=None,
):
    court = Courts(
        name=name,
        sports_type=sports_type,
        description=description,
        created_at=created_at,
        updated_at=updated_at
    )

    db.add(court)
    db.commit()
    db.refresh(court)

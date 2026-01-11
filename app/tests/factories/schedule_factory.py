from datetime import datetime, timezone
from app.models.schedule import Schedules


def schedule_factory(
    db,
    *,
    court_id: int,
    date: str = "2025-01-10",
    start_time: str = "08:00",
    end_time: str = "09:00",
    available: bool = True,
):
    schedule = Schedules(
        court_id=court_id,
        date=date,
        start_time=start_time,
        end_time=end_time,
        available=available,
        created_at=datetime.now(timezone.utc).isoformat(),
        updated_at=None,
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

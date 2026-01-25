from datetime import datetime, timezone, timedelta
from app.models.schedule import Schedule


def schedule_factory(
    db,
    court_id: int,
    date=None,
    start_time="10:00",
    end_time="11:00"
):
    if date is None:
        date = (datetime.now(timezone.utc) + timedelta(days=1)).date().isoformat()
    
    schedule = Schedule(
        court_id=court_id,
        date=date,
        start_time=start_time,
        end_time=end_time,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule

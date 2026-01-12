from app.tests.factories.user_factory import user_factory
from app.tests.factories.court_factory import court_factory
from app.tests.factories.schedule_factory import schedule_factory
from app.tests.factories.reservation_factory import reservation_factory


def test_get_reservation_by_id(client, db):
    user = user_factory(db)
    court = court_factory(db)

    schedule = schedule_factory(db, court_id=court.id)

    reservation = reservation_factory(
        db,
        user_id=user.id,
        schedule_id=schedule.id
    )

    response = client.get(f"/reservations/{reservation.id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == reservation.id

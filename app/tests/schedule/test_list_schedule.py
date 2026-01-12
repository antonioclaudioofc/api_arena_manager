from app.tests.factories.court_factory import court_factory
from app.tests.factories.schedule_factory import schedule_factory


def test_can_list_schedules(client, db):
    court_factory(db)

    schedule_factory(
        db,
        court_id=1,
        start_time="08:00",
        end_time="09:00"
    )

    response = client.get("/schedules")

    assert response.status_code == 200


def test_get_schedule_by_id(client, db):
    court_factory(db)

    schedule_factory(
        db,
        court_id=1,
        start_time="10:00",
        end_time="11:00"
    )

    response = client.get("/schedules/1")

    assert response.status_code == 200

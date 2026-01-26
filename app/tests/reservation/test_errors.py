from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, login, auth_headers, schedule_factory


def test_cannot_create_reservation_without_required_fields(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    payload = {}

    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )

    assert response.status_code == 400


def test_invalid_schedule_id_type(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    payload = {
        "schedule_id": "invalid"
    }

    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )

    assert response.status_code == 400


def test_cannot_reserve_already_reserved_schedule(db, client):
    client1 = user_factory(db)
    client2 = user_factory(db)
    token1 = login(client, client1.username)
    token2 = login(client, client2.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response1 = client.post(
        "/reservations",
        json={"schedule_id": schedule.id},
        headers=auth_headers(token1)
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/reservations",
        json={"schedule_id": schedule.id},
        headers=auth_headers(token2)
    )

    assert response2.status_code == 400

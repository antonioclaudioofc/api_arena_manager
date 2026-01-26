from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, login, auth_headers, schedule_factory


def test_client_can_create_reservation(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.post(
        "/reservations",
        json={"schedule_id": schedule.id},
        headers=auth_headers(token)
    )

    assert response.status_code == 201


def test_client_cannot_make_reservation_without_auth(db, client):
    user = user_factory(db)
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.post("/reservations", json={"schedule_id": schedule.id})

    assert response.status_code == 401


def test_owner_cannot_create_reservation(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.post(
        "/reservations",
        json={"schedule_id": schedule.id},
        headers=auth_headers(token)
    )

    assert response.status_code == 403


def test_cannot_create_reservation_for_past_date(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, yesterday.isoformat(), "10:00", "11:00")

    response = client.post(
        "/reservations",
        json={"schedule_id": schedule.id},
        headers=auth_headers(token)
    )

    assert response.status_code == 400


def test_cannot_create_reservation_for_nonexistent_schedule(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    response = client.post(
        "/reservations",
        json={"schedule_id": 999},
        headers=auth_headers(token)
    )

    assert response.status_code == 404

from datetime import datetime, timezone, timedelta
from app.models.reservation import Reservation
from . import user_factory, arena_factory, court_factory, login, auth_headers, schedule_factory, reservation_factory


def test_client_can_list_own_reservations(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")
    reservation = reservation_factory(db, client_user.id, schedule.id)

    response = client.get(
        "/reservations",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["schedule_id"] == schedule.id


def test_client_only_sees_own_reservations(db, client):
    client1 = user_factory(db)
    client2 = user_factory(db)
    token = login(client, client1.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule1 = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")
    reservation_factory(db, client1.id, schedule1.id)

    schedule2 = schedule_factory(
        db, court.id, tomorrow.isoformat(), "12:00", "13:00")
    reservation_factory(db, client2.id, schedule2.id)

    response = client.get(
        "/reservations/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["client_id"] == client1.id


def test_list_reservations_empty(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    response = client.get(
        "/reservations/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_reservations_returns_correct_fields(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "14:00", "15:00")
    reservation = reservation_factory(db, client_user.id, schedule.id)

    response = client.get(
        "/reservations/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    data = response.json()[0]

    assert "id" in data
    assert "client_id" in data
    assert "schedule_id" in data
    assert "status" in data
    assert "created_at" in data


def test_owner_can_list_reservations_for_own_arena(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)
    client_user = user_factory(db)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "16:00", "17:00")
    reservation_factory(db, client_user.id, schedule.id)

    response = client.get(
        "/reservations/owner",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["client"]["id"] == client_user.id
    assert response.json()[0]["court"]["id"] == court.id
    assert response.json()[0]["arena"]["id"] == arena.id


def test_client_cannot_list_owner_reservations(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    response = client.get(
        "/reservations/owner",
        headers=auth_headers(token)
    )

    assert response.status_code == 403

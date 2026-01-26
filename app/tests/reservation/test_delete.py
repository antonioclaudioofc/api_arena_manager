from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, login, auth_headers, schedule_factory, reservation_factory


def test_client_can_cancel_own_reservation(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(db, court.id, tomorrow.isoformat(), "10:00", "11:00")
    reservation = reservation_factory(db, client_user.id, schedule.id)

    response = client.delete(
        f"/reservations/{reservation.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 204


def test_cannot_cancel_reservation_without_auth(db, client):
    response = client.delete("/reservations/999")

    assert response.status_code == 401


def test_cannot_cancel_other_users_reservation(db, client):
    client1 = user_factory(db)
    client2 = user_factory(db)
    token = login(client, client1.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(db, court.id, tomorrow.isoformat(), "10:00", "11:00")
    reservation = reservation_factory(db, client2.id, schedule.id)

    response = client.delete(
        f"/reservations/{reservation.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 403


def test_cannot_cancel_nonexistent_reservation(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)

    response = client.delete(
        "/reservations/999",
        headers=auth_headers(token)
    )

    assert response.status_code == 404


def test_owner_cannot_cancel_reservation(db, client):
    owner = user_factory(db)
    client_user = user_factory(db)
    owner_token = login(client, owner.username)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    schedule = schedule_factory(db, court.id, tomorrow.isoformat(), "10:00", "11:00")
    reservation = reservation_factory(db, client_user.id, schedule.id)

    response = client.delete(
        f"/reservations/{reservation.id}",
        headers=auth_headers(owner_token)
    )

    assert response.status_code == 403

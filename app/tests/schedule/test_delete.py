from datetime import datetime, timezone, timedelta
from app.models.schedule import Schedule
from . import user_factory, arena_factory, court_factory, login, auth_headers, schedule_factory


def test_owner_can_delete_own_schedule(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.delete(
        f"/schedules/{schedule.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 204


def test_admin_can_delete_any_schedule(db, client):
    admin = user_factory(db, role="admin")
    token = login(client, admin.username)

    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.delete(
        f"/schedules/{schedule.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 204


def test_cannot_delete_schedule_without_auth(db, client):
    response = client.delete("/schedules/999")

    assert response.status_code == 401


def test_client_cannot_delete_schedule(db, client):
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)

    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.delete(
        f"/schedules/{schedule.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 403


def test_owner_cannot_delete_other_owner_schedule(db, client):
    owner1 = user_factory(db, role="owner")
    owner2 = user_factory(db, role="owner")
    token = login(client, owner1.username)

    arena = arena_factory(db, owner2.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.delete(
        f"/schedules/{schedule.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 403


def test_cannot_delete_nonexistent_schedule(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)

    response = client.delete(
        "/schedules/999",
        headers=auth_headers(token)
    )

    assert response.status_code == 404

from datetime import datetime, timezone, timedelta
from app.models.schedule import Schedule
from . import user_factory, arena_factory, court_factory, login, auth_headers, schedule_factory


def test_owner_can_list_own_schedules(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule_factory(db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.get(
        "/schedules",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["court_id"] == court.id


def test_admin_can_list_all_schedules(db, client):
    admin = user_factory(db, role="admin")
    token = login(client, admin.username)

    owner1 = user_factory(db, role="owner")
    owner2 = user_factory(db, role="owner")

    arena1 = arena_factory(db, owner1.id)
    arena2 = arena_factory(db, owner2.id)

    court1 = court_factory(db, arena1.id)
    court2 = court_factory(db, arena2.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule_factory(db, court1.id, tomorrow.isoformat(), "10:00", "11:00")

    schedule_factory(db, court2.id, tomorrow.isoformat(), "12:00", "13:00")

    response = client.get(
        "/schedules",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_client_cannot_list_schedules(db, client):
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)

    response = client.get(
        "/schedules",
        headers=auth_headers(token)
    )

    assert response.status_code == 403


def test_cannot_list_schedules_without_auth(db, client):
    response = client.get("/schedules")

    assert response.status_code == 401


def test_list_schedules_empty(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)

    response = client.get(
        "/schedules",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json() == []


def test_list_schedules_returns_correct_fields(db, client):
    owner = user_factory(db, role="owner")
    token = login(client, owner.username)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()

    schedule = schedule_factory(
        db, court.id, tomorrow.isoformat(), "10:00", "11:00")

    response = client.get(
        "/schedules",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    data = response.json()[0]

    assert "id" in data
    assert "court_id" in data
    assert "date" in data
    assert "start_time" in data
    assert "end_time" in data
    assert "is_available" not in data 

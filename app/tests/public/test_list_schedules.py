from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, schedule_factory, login, auth_headers


def test_list_public_schedules_by_court_without_auth(db, client):
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    schedule_factory(db, court.id)
    schedule_factory(db, court.id, start_time="12:00", end_time="13:00")
    response = client.get(f"/public/courts/{court.id}/schedules")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_public_schedules_with_auth(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    schedule_factory(db, court.id)

    response = client.get(
        f"/public/courts/{court.id}/schedules",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_public_schedules_empty(db, client):
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    response = client.get(f"/public/courts/{court.id}/schedules")

    assert response.status_code == 200
    assert response.json() == []


def test_list_public_schedules_nonexistent_court(db, client):
    response = client.get("/public/courts/999/schedules")

    assert response.status_code == 404


def test_list_public_schedules_returns_correct_fields(db, client):
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    schedule = schedule_factory(db, court.id)

    db.add(schedule)
    db.commit()

    response = client.get(f"/public/courts/{court.id}/schedules")

    assert response.status_code == 200
    data = response.json()[0]

    assert "id" in data
    assert "date" in data
    assert "start_time" in data
    assert "end_time" in data
    assert "court_id" in data

    assert data["court_id"] == court.id
    assert data["start_time"] == "10:00"
    assert data["end_time"] == "11:00"

from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, login, auth_headers


def test_owner_can_create_schedule(db, client):
    owner = user_factory(db)
    token = login(client, owner.username)
    
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/schedules",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 201
    assert response.json()["court_id"] == court.id


def test_owner_can_create_schedule(db, client):
    owner = user_factory(db)
    token = login(client, owner.username)
    
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "14:00",
        "end_time": "15:00"
    }
    
    response = client.post(
        "/schedules",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 201


def test_client_cannot_create_schedule(db, client):
    client_user = user_factory(db)
    token = login(client, client_user.username)
    
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/schedules",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 403


def test_cannot_create_schedule_without_auth(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post("/schedules", json=payload)
    
    assert response.status_code == 401


def test_owner_cannot_create_schedule_for_other_owner_court(db, client):
    owner1 = user_factory(db)
    owner2 = user_factory(db)
    token = login(client, owner1.username)
    
    arena = arena_factory(db, owner2.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/schedules",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 403

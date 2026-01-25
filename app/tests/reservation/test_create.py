"""
Testes para POST /reservations (criar reserva)
"""
from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, login, auth_headers


def test_client_can_create_reservation(db, client):
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
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
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 201
    assert response.json()["court_id"] == court.id
    assert response.json()["date"] == tomorrow.isoformat()


def test_client_cannot_make_reservation_without_auth(db, client):
    """Teste: Sem autenticação não pode fazer reserva"""
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post("/reservations", json=payload)
    
    assert response.status_code == 401


def test_owner_cannot_create_reservation(db, client):
    """Teste: Owner não pode criar reserva"""
    owner = user_factory(db, role="owner")
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
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 403


def test_admin_cannot_create_reservation(db, client):
    """Teste: Admin não pode criar reserva"""
    admin = user_factory(db, role="admin")
    token = login(client, admin.username)
    
    owner = user_factory(db, role="owner")
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
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 403


def test_cannot_create_reservation_for_past_date(db, client):
    """Teste: Não pode fazer reserva para data passada"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    yesterday = (datetime.now(timezone.utc) - timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": yesterday.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 400


def test_cannot_create_reservation_for_today(db, client):
    """Teste: Não pode fazer reserva para hoje"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    today = datetime.now(timezone.utc).date()
    
    payload = {
        "court_id": court.id,
        "date": today.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 400


def test_cannot_create_reservation_for_nonexistent_court(db, client):
    """Teste: Não pode fazer reserva para quadra inexistente"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": 999,
        "date": tomorrow.isoformat(),
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 404

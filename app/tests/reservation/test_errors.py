"""
Testes de erros para reservas
"""
from datetime import datetime, timezone, timedelta
from . import user_factory, arena_factory, court_factory, login, auth_headers


def test_cannot_create_reservation_without_required_fields(db, client):
    """Teste: Faltam campos obrigatórios"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    payload = {
        "court_id": 1
        # Falta date, start_time, end_time
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 422


def test_invalid_time_format(db, client):
    """Teste: Formato de hora inválido"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "25:00",  # Hora inválida
        "end_time": "11:00"
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 422


def test_end_time_before_start_time(db, client):
    """Teste: Hora de término antes do início"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    payload = {
        "court_id": court.id,
        "date": tomorrow.isoformat(),
        "start_time": "11:00",
        "end_time": "10:00"  # Antes do início
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 400


def test_invalid_date_format(db, client):
    """Teste: Formato de data inválido"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    payload = {
        "court_id": court.id,
        "date": "2026-13-45",  # Data inválida
        "start_time": "10:00",
        "end_time": "11:00"
    }
    
    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers(token)
    )
    
    assert response.status_code == 422

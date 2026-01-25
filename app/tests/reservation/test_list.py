"""
Testes para GET /reservations (listar reservas do usuário)
"""
from datetime import datetime, timezone, timedelta
from app.models.reservation import Reservation
from . import user_factory, arena_factory, court_factory, login, auth_headers


def test_client_can_list_own_reservations(db, client):
    """Teste: Cliente pode listar suas próprias reservas"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    reservation = Reservation(
        client_id=client_user.id,
        court_id=court.id,
        date=tomorrow.isoformat(),
        start_time="10:00",
        end_time="11:00",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(reservation)
    db.commit()
    
    response = client.get(
        "/reservations",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["court_id"] == court.id


def test_cannot_list_reservations_without_auth(db, client):
    """Teste: Sem autenticação não pode listar"""
    response = client.get("/reservations")
    
    assert response.status_code == 401


def test_client_only_sees_own_reservations(db, client):
    """Teste: Cliente só vê suas próprias reservas"""
    client1 = user_factory(db, role="client")
    client2 = user_factory(db, role="client")
    token = login(client, client1.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    # Reserva do cliente 1
    res1 = Reservation(
        client_id=client1.id,
        court_id=court.id,
        date=tomorrow.isoformat(),
        start_time="10:00",
        end_time="11:00",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    # Reserva do cliente 2
    res2 = Reservation(
        client_id=client2.id,
        court_id=court.id,
        date=tomorrow.isoformat(),
        start_time="12:00",
        end_time="13:00",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(res1)
    db.add(res2)
    db.commit()
    
    response = client.get(
        "/reservations",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["client_id"] == client1.id


def test_list_reservations_empty(db, client):
    """Teste: Listar reservas quando não há nenhuma"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    response = client.get(
        "/reservations",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 200
    assert response.json() == []


def test_list_reservations_returns_correct_fields(db, client):
    """Teste: Validar que retorna os campos corretos"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    reservation = Reservation(
        client_id=client_user.id,
        court_id=court.id,
        date=tomorrow.isoformat(),
        start_time="14:00",
        end_time="15:00",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(reservation)
    db.commit()
    
    response = client.get(
        "/reservations",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 200
    data = response.json()[0]
    
    assert "id" in data
    assert "client_id" in data
    assert "court_id" in data
    assert "date" in data
    assert "start_time" in data
    assert "end_time" in data

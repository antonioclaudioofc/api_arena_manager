"""
Testes para DELETE /reservations/{id} (cancelar reserva)
"""
from datetime import datetime, timezone, timedelta
from app.models.reservation import Reservation
from . import user_factory, arena_factory, court_factory, login, auth_headers


def test_client_can_cancel_own_reservation(db, client):
    """Teste: Cliente pode cancelar sua própria reserva"""
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
    
    response = client.delete(
        f"/reservations/{reservation.id}",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 204


def test_cannot_cancel_reservation_without_auth(db, client):
    """Teste: Sem autenticação não pode cancelar"""
    response = client.delete("/reservations/999")
    
    assert response.status_code == 401


def test_cannot_cancel_other_users_reservation(db, client):
    """Teste: Cliente não pode cancelar reserva de outro"""
    client1 = user_factory(db, role="client")
    client2 = user_factory(db, role="client")
    token = login(client, client1.username)
    
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)
    
    tomorrow = (datetime.now(timezone.utc) + timedelta(days=1)).date()
    
    reservation = Reservation(
        client_id=client2.id,
        court_id=court.id,
        date=tomorrow.isoformat(),
        start_time="10:00",
        end_time="11:00",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    db.add(reservation)
    db.commit()
    
    response = client.delete(
        f"/reservations/{reservation.id}",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 403


def test_cannot_cancel_nonexistent_reservation(db, client):
    """Teste: Não pode cancelar reserva inexistente"""
    client_user = user_factory(db, role="client")
    token = login(client, client_user.username)
    
    response = client.delete(
        "/reservations/999",
        headers=auth_headers(token)
    )
    
    assert response.status_code == 404


def test_owner_cannot_cancel_reservation(db, client):
    """Teste: Owner não pode cancelar reserva do cliente"""
    owner = user_factory(db, role="owner")
    client_user = user_factory(db, role="client")
    owner_token = login(client, owner.username)
    
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
    
    response = client.delete(
        f"/reservations/{reservation.id}",
        headers=auth_headers(owner_token)
    )
    
    assert response.status_code == 403

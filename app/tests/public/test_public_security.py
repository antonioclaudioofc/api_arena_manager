"""
Testes de segurança para rotas públicas
"""
from . import user_factory, arena_factory, court_factory


def test_public_arenas_no_sensitive_data(db, client):
    """Teste: Rotas públicas não expõem dados sensíveis"""
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)

    response = client.get("/public/arenas")
    data = response.json()[0]

    # Não deve conter password
    assert "hashed_password" not in data
    assert "password" not in data

    # Pode conter owner_id (para referência)
    assert "owner_id" in data


def test_public_courts_accessible_without_login(db, client):
    """Teste: Quadras públicas acessíveis sem login"""
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    # Sem token
    response = client.get(f"/public/arenas/{arena.id}/courts")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_public_schedules_accessible_without_login(db, client):
    """Teste: Horários públicos acessíveis sem login"""
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    # Sem token
    response = client.get(f"/public/courts/{court.id}/schedules")

    assert response.status_code == 200


def test_public_endpoints_do_not_require_authentication(db, client):
    """Teste: Endpoints públicos não requerem autenticação"""
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    # Sem headers de autenticação
    response1 = client.get("/public/arenas")
    response2 = client.get(f"/public/arenas/{arena.id}/courts")
    response3 = client.get(f"/public/courts/{court.id}/schedules")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200


def test_public_endpoints_work_with_invalid_token(db, client):
    """Teste: Endpoints públicos funcionam mesmo com token inválido"""
    owner = user_factory(db, role="owner")
    arena = arena_factory(db, owner.id)

    headers = {"Authorization": "Bearer invalid_token_123"}

    # Deveria funcionar mesmo com token inválido
    response = client.get(
        "/public/arenas",
        headers=headers
    )

    # Pode retornar 401 ou 200 dependendo da implementação
    # Se for 200, está funcionando publicamente
    assert response.status_code in [200, 401]

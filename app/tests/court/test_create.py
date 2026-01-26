from . import user_factory, arena_factory, auth_headers, login


def test_owner_can_create_court(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    arena = arena_factory(db, user.id)

    response = client.post(
        "/courts",
        headers=auth_headers(token),
        json={
            "arena_id": arena.id,
            "name": "Quadra A",
            "sports_type": "Vôleiball",
            "price_per_hour": 99.99,
        }
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Quadra criada com sucesso"


def test_create_court_unauthorized(db, client):
    user = user_factory(db)
    arena = arena_factory(db, user.id)

    response = client.post(
        "/courts",
        json={
            "name": "Quadra A",
            "arena_id": arena.id,
            "sports_type": "Basquete",
            "price_per_hour": 81.21,
        }
    )

    assert response.status_code == 401


def test_create_court_not_owner(db, client):
    owner = user_factory(db)
    user = user_factory(db)

    arena = arena_factory(db, owner.id)

    token = login(client, user.username)

    response = client.post(
        "/courts",
        headers=auth_headers(token),
        json={
            "name": "Quadra A",
            "arena_id": arena.id,
            "sports_type": "Basquete",
            "price_per_hour": 81.21,
        }
    )

    assert response.status_code == 403


def test_create_court_arena_not_found(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    response = client.post(
        "/courts",
        headers=auth_headers(token),
        json={
            "name": "Quadra A",
            "arena_id": "1",
            "sports_type": "Basquete",
            "price_per_hour": 81.21,
        }
    )

    assert response.status_code == 404

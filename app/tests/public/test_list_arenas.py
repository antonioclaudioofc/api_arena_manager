from . import user_factory, arena_factory, login, auth_headers


def test_list_public_arenas_without_auth(db, client):
    owner = user_factory(db, role="owner")
    arena_factory(db, owner.id, name="Arena 1")
    arena_factory(db, owner.id, name="Arena 2")

    response = client.get("/public/arenas")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] in ["Arena 1", "Arena 2"]


def test_list_public_arenas_with_auth(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    owner = user_factory(db, role="owner")
    arena_factory(db, owner.id, name="Arena Test")

    response = client.get(
        "/public/arenas",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_list_public_arenas_empty(db, client):
    response = client.get("/public/arenas")

    assert response.status_code == 200
    assert response.json() == []


def test_get_specific_public_arena(db, client):
    owner = user_factory(db, role="owner")
    arena = arena_factory(
        db, owner.id, name="Arena Especial", city="São Paulo")

    response = client.get(f"/public/arenas/{arena.id}")

    assert response.status_code == 200
    assert response.json()["name"] == "Arena Especial"
    assert response.json()["city"] == "São Paulo"


def test_get_nonexistent_public_arena(db, client):
    response = client.get("/public/arenas/999")

    assert response.status_code == 404

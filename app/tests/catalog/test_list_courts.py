from . import user_factory, arena_factory, court_factory, login, auth_headers


def test_list_catalog_courts_by_arena_without_auth(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)

    court_factory(db, arena.id, name="Quadra 1")
    court_factory(db, arena.id, name="Quadra 2")

    response = client.get(f"/catalog/arenas/{arena.id}/courts")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] in ["Quadra 1", "Quadra 2"]


def test_list_catalog_courts_by_arena_with_auth(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court_factory(db, arena.id, name="Quadra Auth")

    response = client.get(
        f"/catalog/arenas/{arena.id}/courts",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Quadra Auth"


def test_list_catalog_courts_empty(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)

    response = client.get(f"/catalog/arenas/{arena.id}/courts")

    assert response.status_code == 200
    assert response.json() == []


def test_list_catalog_courts_nonexistent_arena(db, client):
    response = client.get("/catalog/arenas/999/courts")

    assert response.status_code == 404


def test_list_catalog_courts_returns_correct_fields(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(
        db,
        arena.id,
        name="Quadra Premium",
        sports_type="Futsal",
        price_per_hour=150.00
    )

    response = client.get(f"/catalog/arenas/{arena.id}/courts")

    assert response.status_code == 200
    data = response.json()[0]

    assert "id" in data
    assert "name" in data
    assert "arena_id" in data
    assert "sports_type" in data
    assert "price_per_hour" in data

    assert data["id"] == court.id
    assert data["name"] == "Quadra Premium"
    assert data["sports_type"] == "Futsal"
    assert float(data["price_per_hour"]) == 150.00

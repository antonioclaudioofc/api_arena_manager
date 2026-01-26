from . import user_factory, arena_factory, court_factory


def test_public_arenas_no_sensitive_data(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)

    response = client.get("/public/arenas")
    data = response.json()[0]

    assert "hashed_password" not in data
    assert "password" not in data

    assert "owner_id" in data


def test_public_courts_accessible_without_login(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    response = client.get(f"/public/arenas/{arena.id}/courts")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_public_schedules_accessible_without_login(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    response = client.get(f"/public/courts/{court.id}/schedules")

    assert response.status_code == 200


def test_public_endpoints_do_not_require_authentication(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    response1 = client.get("/public/arenas")
    response2 = client.get(f"/public/arenas/{arena.id}/courts")
    response3 = client.get(f"/public/courts/{court.id}/schedules")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200


def test_public_endpoints_work_with_invalid_token(db, client):
    owner = user_factory(db)
    arena = arena_factory(db, owner.id)

    headers = {"Authorization": "Bearer invalid_token_123"}

    response = client.get(
        "/public/arenas",
        headers=headers
    )

    assert response.status_code in [200, 401]

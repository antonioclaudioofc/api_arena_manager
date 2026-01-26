from . import user_factory, arena_factory, court_factory, auth_headers, login


def test_owner_update_court(db, client):
    user = user_factory(db)
    token = login(client, user.username,)

    arena = arena_factory(db, user.id)
    court = court_factory(db, arena.id)

    response = client.put(
        f"/courts/{court.id}",
        headers=auth_headers(token),
        json={
            "name": "Quadra A"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Quadra atualizada com sucesso"


def test_update_court_not_owner(db, client):
    owner = user_factory(db)
    other = user_factory(db)

    arena = arena_factory(db, owner.id)
    court = court_factory(db, arena.id)

    token = login(client, other.username)

    response = client.put(
        f"/courts/{court.id}",
        headers=auth_headers(token),
        json={
            "name": "Quadra A"
        }
    )

    assert response.status_code == 403


def test_update_court_not_found(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    response = client.put(
        "/courts/999",
        headers=auth_headers(token),
        json={
            "name": "Quadra A"
        }
    )

    assert response.status_code == 404

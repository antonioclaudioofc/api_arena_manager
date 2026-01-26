from . import user_factory, login, arena_factory, auth_headers


def test_owner_can_update_own_arena(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    arena = arena_factory(db, user.id)

    response = client.put(
        f"/arenas/{arena.id}",
        headers=auth_headers(token),
        json={
            "name": "Arena B"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Arena atualizada com sucesso"


def test_owner_cannot_update_other_arena(db, client):
    owner1 = user_factory(db)
    owner2 = user_factory(db)

    arena = arena_factory(db, owner2.id)

    token = login(client, owner1.username)

    response = client.put(
        f"/arenas/{arena.id}",
        headers=auth_headers(token),
        json={
            "name": "Quadra A"
        }
    )

    assert response.status_code == 403


def test_update_arena_not_found(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    response = client.put(
        "/arenas/091",
        headers=auth_headers(token),
        json={
            "name": "Quadra B"
        }
    )

    assert response.status_code == 404

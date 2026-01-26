from . import user_factory, login, arena_factory, auth_headers


def test_owner_list_own_arenas(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    arena_factory(db, user.id)
    arena_factory(db, user.id)

    response = client.get(
        "/arenas",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_client_cannot_list_arenas(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    response = client.get(
        "/arenas",
        headers=auth_headers(token)
    )

    assert response.status_code == 403

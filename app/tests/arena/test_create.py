from . import user_factory, login, auth_headers


def test_create_arena_promotes_user_to_owner(db, client):
    user = user_factory(db)

    token = login(client, user.username)

    response = client.post(
        "/arenas",
        headers=auth_headers(token),
        json={
            "name": "Arena B",
            "city": "Ceára",
            "address": "Rua 4"
        }
    )

    assert response.status_code == 201
    assert user.role == "owner"


def test_create_arena_unauthorized(client):
    response = client.post(
        "/arenas",
        json={
            "name": "Arena C",
            "city": "Piaui",
            "address": "Rua 12"
        }
    )

    assert response.status_code == 401

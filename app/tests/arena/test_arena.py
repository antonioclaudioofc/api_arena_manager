from app.tests.factories.arena_factory import arena_factory
from app.tests.factories.user_factory import user_factory
from app.tests.utils.auth import auth_headers, login


def test_create_arena_promotes_user_to_owner(db, client):
    user = user_factory(db)

    token = login(client, user.username, "123456")

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

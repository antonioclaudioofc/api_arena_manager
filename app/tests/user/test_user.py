from app.tests.factories.user_factory import user_factory
from app.tests.utils.auth import auth_headers, login


def test_get_profile(client, db):
    user = user_factory(db)

    token = login(client, user.username, "123456")

    response = client.get(
        "/user/me",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert response.json()["email"] == user.email


def test_get_profile_unauthorized(client):
    response = client.get("/user/me")

    assert response.status_code == 401


def test_update_profile(client, db):
    user = user_factory(db)

    token = login(client, user.username, "123456")

    response = client.put(
        "/user/me",
        headers=auth_headers(token),
        json={
            "name": "Antonio"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Perfil atualizado com sucesso"


def test_change_password_wrong_password(client, db):
    user = user_factory(db)

    token = login(client, user.username, "123456")

    response = client.put(
        "user/change-password",
        headers=auth_headers(token),
        json={
            "password": "errada",
            "new_password": "90898237"
        }
    )

    assert response.status_code == 403

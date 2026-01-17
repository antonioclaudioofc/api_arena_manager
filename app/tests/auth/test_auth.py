def test_register_sucess(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "username": "user_test",
            "name": "User Test",
            "password": "123456",
            "role": "client"
        }
    )

    assert response.status_code == 201


def test_register_email_already_exists(client):
    payload = {
        "email": "email_exists@test.com",
        "username": "user_exists",
        "name": "User Exists",
        "password": "123456",
        "role": "client",
    }

    client.post("/auth/register", json=payload)
    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "user",
            "password": "user"
        }
    )

    assert response.status_code == 401

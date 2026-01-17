def login(client, username, password):
    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def auth_headers(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }

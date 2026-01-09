def test_user_can_be_login(client, create_user):
    user = create_user()

    response = client.post("/auth/token", data={
        "username": user["username"],
        "password": "123456"
    })

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert body["token_type"] == "bearer"

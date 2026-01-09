def test_user_can_be_get_profile(client, auth_headers):
    response = client.get(
        "/user/me",
        headers=auth_headers
    )

    assert response.status_code == 200

    assert "email" in response.json()
    assert "username" in response.json()

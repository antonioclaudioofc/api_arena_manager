def test_get_profile_unathorized(client):
    response = client.get("/user/me")

    assert response.status_code == 401

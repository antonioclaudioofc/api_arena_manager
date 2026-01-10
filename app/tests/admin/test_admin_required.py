def test_admin_routes_require_auth(client):
    response = client.get("/admin/users")
    assert response.status_code == 401


def test_admin_routes_require_admin(client, auth_headers):
    response = client.get(
        "/admin/users",
        headers=auth_headers
    )

    assert response.status_code == 403
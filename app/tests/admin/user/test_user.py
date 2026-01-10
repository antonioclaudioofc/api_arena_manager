def test_admin_can_list_users(client, admin_headers):
    response = client.get(
        "/admin/users",
        headers=admin_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

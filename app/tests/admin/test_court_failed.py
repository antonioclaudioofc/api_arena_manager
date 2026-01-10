def test_client_cannot_create_court(client, auth_headers):
    payload = {
        "name": "Quadra inexistente",
        "sports_type": "futebol, võlei",
    }

    response = client.post(
        "/admin/courts",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 403

def test_admin_can_create_court(client, admin_headers):
    payload = {
        "name": "Quadra Teste",
        "sports_type": "Futebol",
        "description": "Quadra de areia"
    }

    response = client.post(
        "/admin/courts",
        json=payload,
        headers=admin_headers
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Quadra criada com sucesso"

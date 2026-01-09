def test_user_can_be_update_profile(client, auth_headers):
    payload = {
        "first_name": "NovoNome"
    }

    response = client.put(
        "/user/me",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Perfil atualizado com sucesso"

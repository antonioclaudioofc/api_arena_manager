def test_user_can_be_created(client):

    payload = {
        "email": "teste@gmail.com",
        "username": "teste",
        "first_name": "Teste",
        "last_name": "User",
        "password": "123456",
        "role": "client"
    }

    response = client.post(
        "/auth",
        json=payload
    )

    assert response.status_code == 201

    assert response.json() == {
        "message": "Usuário criado com sucesso"
    }

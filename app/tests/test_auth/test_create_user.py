import uuid


def test_user_can_be_created(client):
    payload = {
        "email": f"{uuid.uuid4()}@gmail.com",
        "username": f"user_{uuid.uuid4().hex[:8]}",
        "first_name": "Teste",
        "last_name": "User",
        "password": "123456"
    }

    response = client.post("/auth", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert "message" in data
    assert data["message"] == "Usuário criado com sucesso"

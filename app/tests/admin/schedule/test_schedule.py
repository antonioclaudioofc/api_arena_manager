def test_admin_can_create_schedule(client, admin_headers):
    court = {
        "name": "Arena Z",
        "sports_type": "futsal"
    }

    client.post(
        "/admin/courts",
        json=court,
        headers=admin_headers
    )

    payload = {
        "court_id": 1,
        "date": "2026-01-10",
        "start_time": "08:00",
        "end_time": "09:00",
        "available": True
    }

    response = client.post(
        "/admin/schedules",
        json=payload,
        headers=admin_headers
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Horário criado com sucesso"

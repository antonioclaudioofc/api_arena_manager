def test_admin_can_create_schedule_batch(client, admin_headers):

    client.post(
        "/admin/courts",
        json={
            "name": "Quadra AAA",
            "sports_type": "vôlei"
        },
        headers=admin_headers
    )

    payload = {
        "court_id": 1,
        "start_date": "2026-01-01",
        "end_date": "2026-01-07",
        "start_time": "08:00",
        "end_time": "10:00",
        "interval_minutes": 60,
        "weekdays": [0, 2, 4],
        "months": [1]
    }

    response = client.post(
        "/admin/schedules/batch",
        json=payload,
        headers=admin_headers
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Horários criados com sucesso"

from app.tests.factories import court_factory, reservation_factory, schedule_factory, user_factory


def test_user_can_create_reservation(client, db, auth_headers):
    user = user_factory(db)
    court = court_factory(db)

    schedule = schedule_factory(db, court_id=court.id)

    payload = {
        "schedule_id": schedule.id
    }

    response = client.post(
        "/reservations",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 201

    data = response.json()
    assert data["status"] == "Reservado"
    assert data["schedule"]["id"] == schedule.id


def test_get_reservation_by_id(client, db, auth_headers):
    user = user_factory(db)
    court = court_factory(db)

    schedule = schedule_factory(db, court_id=court.id)

    reservation = reservation_factory(
        db=db,
        user_id=user.id,
        schedule_id=schedule.id
    )

    response = client.get(
        f"/reservations/{reservation.id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == reservation.id

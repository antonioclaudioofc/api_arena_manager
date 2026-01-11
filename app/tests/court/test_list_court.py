from app.tests.factories import court_factory


def test_can_list_courts(client, db):
    court_factory(db)

    response = client.get("/courts")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Quadra A"

def test_list_multiple_courts(client, db):
    court_factory(db)
    court_factory(db, name="Quadra B")

    response = client.get("/courts")

    assert response.status_code == 200
    assert len(response.json()) == 2
from . import user_factory, login, arena_factory, court_factory, auth_headers


def test_owner_list_courts_of_arena(db, client):
    user = user_factory(db)
    token = login(client, user.username)

    arena = arena_factory(db, user.id)
    court_factory(db, arena.id)
    court_factory(db, arena.id)

    response = client.get(
        f"/courts/{arena.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_courts_not_owner(db, client):
    owner = user_factory(db)
    other = user_factory(db)

    arena = arena_factory(db, owner.id)

    token = login(client, other.username)

    response = client.get(
        f"/courts/{arena.id}",
        headers=auth_headers(token)
    )

    assert response.status_code == 403

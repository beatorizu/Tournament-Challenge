import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_can_access_root():
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_can_create_tournament():
    response = client.post("/tournament", json={"name": "Wood Gladiators"})

    assert response.status_code == 200
    assert response.json()["id"] is not None


def test_can_retrieve_tournament_by_id():
    expected_response = {
        "id": "8581c72f-bc5d-4087-aaf8-2ef70c8bd542",
        "name": "Wood Gladiators"
    }

    response = client.get(f"/tournament/{expected_response['id']}")

    assert response.status_code == 200
    assert response.json() == expected_response


def test_cannot_retrieve_tournament_by_id():
    response = client.get("/tournament/aff785a5-9341-4b1f-9cbe-b67c18ba728c")

    assert response.status_code == 404


@pytest.mark.parametrize("name", ['Lorem', 'Ipsum', 'Dolor', 'Sit', 'Amet', 'Consectetur', 'Adipiscing', 'Elit', 'Sed', 'Do', 'Eiusmod', 'Tempor', 'Incididunt', 'Ut', 'Labore', 'Et'])
def test_can_register_competitor(name):
    response = client.post("/tournament/8581c72f-bc5d-4087-aaf8-2ef70c8bd542/competitor", json={"name": name})

    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["name"] == name


def test_can_retrieve_competitor():
    expected_body = {
        "id": "a1227978-1ae1-4279-bb08-fdc2b7ff1c8b",
        "name": "Sed",
        "eliminated": False
    }

    response = client.get("/tournament/01255f28-ba4a-4a9a-bf91-3178d3b0b6f3/competitor/a1227978-1ae1-4279-bb08-fdc2b7ff1c8b")

    assert response.status_code == 200
    assert response.json() == expected_body


def test_can_retrieve_match():
    response = client.get("/tournament/01255f28-ba4a-4a9a-bf91-3178d3b0b6f3/match")

    assert response.status_code == 200


def test_can_register_match_result():
    competitor_a_status = {
        "id": "aed0f2be-5100-4a98-a240-d9a1693ad2ab",
        "name": "Lorem",
        "eliminated": True
    }

    competitor_b_status = {
        "id": "a1227978-1ae1-4279-bb08-fdc2b7ff1c8b",
        "name": "Sed",
        "eliminated": False
    }

    response = client.post(
        "/tournament/01255f28-ba4a-4a9a-bf91-3178d3b0b6f3/match/770c6f66-fe61-4429-b018-14b6d8ca3578",
        json={"competitor_a": {"eliminated": True}, "competitor_b": {"eliminated": False}})

    assert response.status_code == 200

    response_competitor_a_status = client.get(f"/tournament/01255f28-ba4a-4a9a-bf91-3178d3b0b6f3/competitor/{competitor_a_status['id']}")
    response_competitor_b_status = client.get(f"/tournament/01255f28-ba4a-4a9a-bf91-3178d3b0b6f3/competitor/{competitor_b_status['id']}")
    assert response_competitor_a_status.json() == competitor_a_status
    assert response_competitor_b_status.json() == competitor_b_status
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
    assert response.content["id"] is not None


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

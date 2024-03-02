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

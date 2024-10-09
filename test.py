from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_user():
    responce = client.post("/register", json= {
        "name": "h1111ello",
        "email": "he111llo@example.com",
        "password": "he111llo"
    })

    assert responce.status_code == 200
    assert responce.json()["name"] == "h1111ello"



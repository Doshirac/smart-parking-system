from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_spot():
    response = client.post("/spots", json={
        "spot_number": 101,
        "spot_type": "compact",
        "hourly_rate": 3.5
    })
    assert response.status_code == 200
    assert response.json()["spot_type"] == "compact"

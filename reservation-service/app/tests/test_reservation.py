from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta

client = TestClient(app)

def test_create_reservation():
    response = client.post("/reservations", json={
        "user_id": 1,
        "spot_id": 2,
        "start_time": datetime.utcnow().isoformat(),
        "end_time": (datetime.utcnow() + timedelta(hours=1)).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["status"] == "reserved"

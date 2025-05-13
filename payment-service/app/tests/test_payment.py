from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_transaction():
    response = client.post("/transactions", json={
        "reservation_id": 1,
        "user_id": 2,
        "amount": 10.5,
        "payment_method": "Visa"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"

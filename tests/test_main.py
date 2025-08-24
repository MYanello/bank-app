from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.text == '"OK"' or response.text == 'OK'

def test_get_orders():
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    assert "orders" in response.json()

def test_create_order():
    payload = {"term": 12, "amount": 1000.0}
    response = client.post("/api/v1/order", json=payload)
    assert response.status_code == 202
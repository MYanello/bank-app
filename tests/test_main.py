def test_health_check(session, client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.text == '"OK"'


def test_get_orders(session, client):
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    assert "orders" in response.json()
    assert response.json()["orders"] == []  # Should be empty initially


def test_create_order(session, client):
    payload = {"term": 12, "amount": 1000.0}
    response = client.post("/api/v1/order", json=payload)
    assert response.status_code == 202


def test_create_and_get_order(session, client):
    # Create an order
    payload = {"term": 24, "amount": 5000.0}
    response = client.post("/api/v1/order", json=payload)
    assert response.status_code == 202

    # Get all orders and verify the order was created
    response = client.get("/api/v1/orders")
    assert response.status_code == 200
    orders = response.json()["orders"]
    assert len(orders) == 1
    assert orders[0]["term"] == 24
    assert orders[0]["amount"] == 5000.0
    assert "submitted" in orders[0]

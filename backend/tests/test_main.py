import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "checks" in data
    assert data["checks"]["api"] == "healthy"


def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 3


def test_get_item_valid():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200

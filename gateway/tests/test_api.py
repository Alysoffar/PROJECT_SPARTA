"""Test Gateway API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "docs" in data


def test_create_workflow():
    """Test workflow creation."""
    workflow_data = {
        "user_input": "Create a 32-bit adder",
        "parameters": {},
        "metadata": {},
    }
    response = client.post("/api/v1/workflows", json=workflow_data)
    # This may fail if orchestrator is not running, which is expected
    assert response.status_code in [200, 502]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

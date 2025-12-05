"""Test Orchestrator."""
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


def test_create_workflow():
    """Test workflow creation."""
    workflow_data = {
        "user_input": "Create a 32-bit adder",
        "parameters": {},
        "metadata": {},
    }
    response = client.post("/workflows", json=workflow_data)
    assert response.status_code == 200
    data = response.json()
    assert "workflow_id" in data
    assert "status" in data


def test_get_workflow_status():
    """Test getting workflow status."""
    # First create a workflow
    workflow_data = {
        "user_input": "Create a multiplier",
        "parameters": {},
        "metadata": {},
    }
    create_response = client.post("/workflows", json=workflow_data)
    assert create_response.status_code == 200
    workflow_id = create_response.json()["workflow_id"]
    
    # Then get its status
    status_response = client.get(f"/workflows/{workflow_id}")
    assert status_response.status_code == 200
    data = status_response.json()
    assert data["workflow_id"] == workflow_id


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

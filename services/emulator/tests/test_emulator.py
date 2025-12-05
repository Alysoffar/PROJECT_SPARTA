"""Test Emulator Service."""
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


def test_run_emulation():
    """Test running emulation."""
    emulation_request = {
        "instructions": [
            {"opcode": "ADD", "operands": ["r1", "r2", "r3"]},
            {"opcode": "LOAD", "operands": ["r4", "0x100"]},
            {"opcode": "NOP", "operands": []},
        ],
        "num_cycles": 10,
        "clock_period_ns": 10.0,
        "config": {},
    }
    response = client.post("/emulate", json=emulation_request)
    assert response.status_code == 200
    data = response.json()
    assert "emulation_id" in data
    assert "status" in data
    assert "cycles_executed" in data
    assert data["cycles_executed"] == 3  # 3 instructions


def test_emulation_with_different_opcodes():
    """Test emulation with various opcodes."""
    emulation_request = {
        "instructions": [
            {"opcode": "ADD", "operands": ["r1", "r0", "r0"]},
            {"opcode": "SUB", "operands": ["r2", "r1", "r0"]},
            {"opcode": "STORE", "operands": ["r1", "0x200"]},
        ],
        "num_cycles": 5,
        "clock_period_ns": 5.0,
    }
    response = client.post("/emulate", json=emulation_request)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert len(data["outputs"]) == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

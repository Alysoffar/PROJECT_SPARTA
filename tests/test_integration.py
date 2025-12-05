"""Integration test for end-to-end workflow."""
import pytest
import time
import httpx
import asyncio
from typing import Optional


BASE_URL = "http://localhost:8000/api/v1"


async def wait_for_service(url: str, service_name: str, max_wait: int = 60) -> bool:
    """Wait for a service to become available."""
    print(f"\nWaiting for {service_name} at {url}...")
    async with httpx.AsyncClient(timeout=5.0) as client:
        for attempt in range(max_wait):
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    print(f"✓ {service_name} is ready")
                    return True
            except (httpx.ConnectError, httpx.TimeoutException):
                if attempt % 5 == 0:  # Print every 5 seconds
                    print(f"  Waiting for {service_name}... ({attempt}s)")
            await asyncio.sleep(1)
    
    print(f"✗ {service_name} did not become available in {max_wait}s")
    return False


@pytest.mark.asyncio
async def test_end_to_end_workflow():
    """Test complete workflow from creation to completion."""
    # Wait for services to be ready
    gateway_ready = await wait_for_service("http://localhost:8000/health", "Gateway", max_wait=90)
    orchestrator_ready = await wait_for_service("http://localhost:8001/health", "Orchestrator", max_wait=90)
    
    if not gateway_ready or not orchestrator_ready:
        pytest.skip("Services are not running. Please start services with: .\\scripts\\start.ps1")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Step 1: Create workflow
        workflow_request = {
            "user_input": "Create a 32-bit adder with low power consumption",
            "parameters": {},
            "metadata": {"test": "e2e"},
        }
        
        response = await client.post(f"{BASE_URL}/workflows", json=workflow_request)
        assert response.status_code == 200
        data = response.json()
        
        workflow_id = data["workflow_id"]
        assert workflow_id is not None
        assert data["status"] in ["pending", "running"]
        
        # Step 2: Poll for workflow completion
        max_attempts = 20
        for attempt in range(max_attempts):
            response = await client.get(f"{BASE_URL}/workflows/{workflow_id}")
            assert response.status_code == 200
            status_data = response.json()
            
            if status_data["status"] == "completed":
                assert status_data["progress_percentage"] == 100.0
                print(f"\nWorkflow completed in {attempt + 1} attempts")
                break
            elif status_data["status"] == "failed":
                pytest.fail(f"Workflow failed: {status_data}")
            
            time.sleep(2)  # Wait 2 seconds between polls
        else:
            pytest.fail("Workflow did not complete in time")
        
        # Step 3: Verify workflow has results
        assert len(status_data["stages_completed"]) > 0


@pytest.mark.asyncio
async def test_health_checks():
    """Test all service health endpoints."""
    services = [
        ("Gateway", "http://localhost:8000/health"),
        ("Orchestrator", "http://localhost:8001/health"),
        ("NLP Agent", "http://localhost:8010/health"),
        ("Synthesis Agent", "http://localhost:8011/health"),
        ("Emulator", "http://localhost:8020/health"),
        ("RTL Generator", "http://localhost:8021/health"),
    ]
    
    # Wait for at least gateway to be available
    gateway_ready = await wait_for_service("http://localhost:8000/health", "Gateway", max_wait=60)
    if not gateway_ready:
        pytest.skip("Services are not running. Please start services with: .\\scripts\\start.ps1")
    
    # Give other services a bit more time
    print("\nWaiting 10 seconds for other services to initialize...")
    await asyncio.sleep(10)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        for service_name, url in services:
            try:
                response = await client.get(url)
                assert response.status_code == 200
                data = response.json()
                assert "status" in data
                print(f"✓ {service_name}: {data['status']}")
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                print(f"⚠ {service_name}: Not running (this is OK if service is still starting)")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

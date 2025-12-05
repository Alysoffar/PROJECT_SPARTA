"""Workflow endpoints."""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
import httpx
from app.config import settings


router = APIRouter()


@router.post("/")
async def create_workflow(request: Dict[str, Any]):
    """Create a new workflow (trailing slash)."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ORCHESTRATOR_URL}/workflows",
                json=request,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Orchestrator error: {str(e)}")


@router.post("")
async def create_workflow_no_slash(request: Dict[str, Any]):
    """Create a new workflow (no trailing slash) to avoid redirects."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.ORCHESTRATOR_URL}/workflows",
                json=request,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Orchestrator error: {str(e)}")


@router.get("/{workflow_id}")
async def get_workflow_status(workflow_id: str):
    """Get workflow status."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.ORCHESTRATOR_URL}/workflows/{workflow_id}",
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Orchestrator error: {str(e)}")


@router.get("/{workflow_id}/result")
async def get_workflow_result(workflow_id: str):
    """Get workflow result with artifacts and outputs."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.ORCHESTRATOR_URL}/workflows/{workflow_id}/result",
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Orchestrator error: {str(e)}")


@router.delete("/{workflow_id}")
async def get_workflow_result(workflow_id: str):
    """Get workflow result with artifacts and outputs."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.ORCHESTRATOR_URL}/workflows/{workflow_id}/result",
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Orchestrator error: {str(e)}")


@router.delete("/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{settings.ORCHESTRATOR_URL}/workflows/{workflow_id}",
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Orchestrator error: {str(e)}")

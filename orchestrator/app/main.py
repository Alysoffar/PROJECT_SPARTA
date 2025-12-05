"""Orchestrator main application."""
import uuid
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.workflow_manager import WorkflowManager
from app.schemas import WorkflowRequest, WorkflowStatus, WorkflowResult


# Global workflow manager
workflow_manager = WorkflowManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    print(f"Starting {settings.SERVICE_NAME} v{settings.VERSION}")
    await workflow_manager.initialize()
    yield
    await workflow_manager.shutdown()
    print(f"Shutting down {settings.SERVICE_NAME}")


app = FastAPI(
    title=settings.SERVICE_NAME,
    version=settings.VERSION,
    description="AI Orchestrator for SPARTA platform",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
        "status": "healthy",
    }


@app.post("/workflows", response_model=WorkflowStatus)
async def create_workflow(request: WorkflowRequest):
    """Create and start a new workflow."""
    workflow_id = request.workflow_id or f"wf-{uuid.uuid4().hex[:12]}"
    
    try:
        status = await workflow_manager.create_workflow(
            workflow_id=workflow_id,
            user_input=request.user_input,
            parameters=request.parameters or {},
            metadata=request.metadata or {},
        )
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/workflows/{workflow_id}", response_model=WorkflowStatus)
async def get_workflow_status(workflow_id: str):
    """Get workflow status."""
    status = await workflow_manager.get_workflow_status(workflow_id)
    if not status:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return status


@app.delete("/workflows/{workflow_id}")
async def cancel_workflow(workflow_id: str):
    """Cancel a running workflow."""
    success = await workflow_manager.cancel_workflow(workflow_id)
    if not success:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_id": workflow_id, "status": "cancelled"}


@app.get("/workflows/{workflow_id}/result", response_model=WorkflowResult)
async def get_workflow_result(workflow_id: str):
    """Get workflow result."""
    result = await workflow_manager.get_workflow_result(workflow_id)
    if not result:
        raise HTTPException(status_code=404, detail="Workflow result not found")
    return result

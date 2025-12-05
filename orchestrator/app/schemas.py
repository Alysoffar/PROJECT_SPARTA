"""Workflow-specific schemas."""
from typing import Optional, Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, Field
import sys
import os

# Add shared schemas to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'shared')))

from schemas.common import TaskStatus
from schemas.orchestration import WorkflowStage


class WorkflowRequest(BaseModel):
    """Workflow creation request."""
    workflow_id: Optional[str] = None
    user_input: str = Field(..., description="Natural language user request")
    stages: List[WorkflowStage] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowStatus(BaseModel):
    """Workflow execution status."""
    workflow_id: str
    current_stage: WorkflowStage
    status: TaskStatus
    progress_percentage: float = Field(ge=0.0, le=100.0)
    stages_completed: List[WorkflowStage] = Field(default_factory=list)
    current_task_id: Optional[str] = None
    started_at: datetime
    updated_at: datetime
    estimated_completion: Optional[datetime] = None


class WorkflowResult(BaseModel):
    """Complete workflow result."""
    workflow_id: str
    status: TaskStatus
    results: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    artifacts: List[str] = Field(default_factory=list)
    errors: Optional[List[str]] = None
    execution_time_ms: float
    completed_at: datetime

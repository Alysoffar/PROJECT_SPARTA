"""Orchestration-specific schemas."""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from .common import TaskStatus


class AgentType(str, Enum):
    """Types of specialized agents."""
    NLP = "nlp"
    SYNTHESIS = "synthesis"
    OPTIMIZATION = "optimization"
    VISUALIZATION = "visualization"


class ServiceType(str, Enum):
    """Types of backend services."""
    EMULATOR = "emulator"
    RTL_GENERATOR = "rtl_generator"
    MODEL_SYNTHESIS = "model_synthesis"
    COMPILER = "compiler"


class WorkflowStage(str, Enum):
    """Workflow execution stages."""
    PARSING = "parsing"
    SYNTHESIS = "synthesis"
    GENERATION = "generation"
    OPTIMIZATION = "optimization"
    EMULATION = "emulation"
    VISUALIZATION = "visualization"
    COMPLETE = "complete"


class AgentTask(BaseModel):
    """Task sent to a specialized agent."""
    task_id: str
    agent_type: AgentType
    operation: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = Field(default=300)


class ServiceTask(BaseModel):
    """Task sent to a backend service."""
    task_id: str
    service_type: ServiceType
    operation: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    context: Dict[str, Any] = Field(default_factory=dict)
    timeout_seconds: int = Field(default=600)


class WorkflowRequest(BaseModel):
    """Orchestrated workflow request."""
    workflow_id: str
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
    results: Dict[WorkflowStage, Dict[str, Any]] = Field(default_factory=dict)
    artifacts: List[str] = Field(default_factory=list)
    errors: Optional[List[str]] = None
    execution_time_ms: float
    completed_at: datetime

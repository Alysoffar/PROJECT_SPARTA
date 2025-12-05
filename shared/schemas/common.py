"""Common data schemas shared across all services."""
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class BaseResponse(BaseModel):
    """Base response model."""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None


class TaskRequest(BaseModel):
    """Generic task request."""
    task_id: str = Field(..., description="Unique task identifier")
    task_type: str = Field(..., description="Type of task to execute")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    """Generic task response."""
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    errors: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    execution_time_ms: Optional[float] = None


class HealthStatus(BaseModel):
    """Service health status."""
    service_name: str
    status: str
    version: str
    uptime_seconds: float
    dependencies: Dict[str, str] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

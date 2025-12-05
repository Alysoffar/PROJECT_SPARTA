"""Hardware-specific data schemas."""
from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field


class DesignLanguage(str, Enum):
    """Hardware description languages."""
    VERILOG = "verilog"
    SYSTEMVERILOG = "systemverilog"
    VHDL = "vhdl"
    CHISEL = "chisel"
    BLUESPEC = "bluespec"


class OptimizationObjective(str, Enum):
    """Optimization objectives."""
    AREA = "area"
    POWER = "power"
    PERFORMANCE = "performance"
    LATENCY = "latency"
    THROUGHPUT = "throughput"


class HardwareSpec(BaseModel):
    """Hardware specification model."""
    spec_id: str = Field(..., description="Specification identifier")
    description: str = Field(..., description="Natural language description")
    target_language: DesignLanguage = Field(default=DesignLanguage.SYSTEMVERILOG)
    constraints: Dict[str, Any] = Field(default_factory=dict)
    optimization_goals: List[OptimizationObjective] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RTLCode(BaseModel):
    """RTL code representation."""
    code_id: str
    language: DesignLanguage
    source_code: str
    module_name: str
    ports: List[Dict[str, Any]] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SimulationConfig(BaseModel):
    """Simulation configuration."""
    config_id: str
    num_cycles: int = Field(default=1000, ge=1)
    clock_period_ns: float = Field(default=10.0, gt=0)
    input_vectors: List[Dict[str, Any]] = Field(default_factory=list)
    trace_signals: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SimulationResult(BaseModel):
    """Simulation result."""
    result_id: str
    success: bool
    cycles_executed: int
    output_values: List[Dict[str, Any]] = Field(default_factory=list)
    waveform_data: Optional[str] = None
    performance_metrics: Dict[str, float] = Field(default_factory=dict)
    errors: Optional[List[str]] = None


class OptimizationRequest(BaseModel):
    """Multi-objective optimization request."""
    request_id: str
    rtl_code: RTLCode
    objectives: List[OptimizationObjective]
    constraints: Dict[str, Any] = Field(default_factory=dict)
    max_iterations: int = Field(default=100, ge=1)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OptimizationResult(BaseModel):
    """Optimization result."""
    result_id: str
    optimized_code: RTLCode
    pareto_front: List[Dict[str, float]] = Field(default_factory=list)
    final_metrics: Dict[str, float] = Field(default_factory=dict)
    iterations_completed: int
    convergence_history: List[Dict[str, float]] = Field(default_factory=list)

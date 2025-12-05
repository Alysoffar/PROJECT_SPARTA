// Shared types for API schemas

export enum TaskStatus {
  PENDING = "pending",
  RUNNING = "running",
  COMPLETED = "completed",
  FAILED = "failed",
  CANCELLED = "cancelled",
}

export enum DesignLanguage {
  VERILOG = "verilog",
  SYSTEMVERILOG = "systemverilog",
  VHDL = "vhdl",
  CHISEL = "chisel",
}

export enum OptimizationObjective {
  AREA = "area",
  POWER = "power",
  PERFORMANCE = "performance",
}

export enum WorkflowStage {
  PARSING = "parsing",
  SYNTHESIS = "synthesis",
  GENERATION = "generation",
  OPTIMIZATION = "optimization",
  EMULATION = "emulation",
  COMPLETE = "complete",
}

export interface WorkflowRequest {
  workflow_id?: string;
  user_input: string;
  stages?: WorkflowStage[];
  parameters?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface WorkflowStatus {
  workflow_id: string;
  current_stage: WorkflowStage;
  status: TaskStatus;
  progress_percentage: number;
  stages_completed: WorkflowStage[];
  current_task_id?: string;
  started_at: string;
  updated_at: string;
  estimated_completion?: string;
}

export interface WorkflowResult {
  workflow_id: string;
  status: TaskStatus;
  results: Record<WorkflowStage, any>;
  artifacts: string[];
  errors?: string[];
  execution_time_ms: number;
  completed_at: string;
}


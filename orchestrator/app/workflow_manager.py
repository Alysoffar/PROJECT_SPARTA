"""Workflow manager for orchestrating tasks."""
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
import httpx

from app.config import settings
from app.schemas import WorkflowStatus, WorkflowResult
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'shared')))
from schemas.common import TaskStatus
from schemas.orchestration import WorkflowStage


class WorkflowManager:
    """Manages workflow lifecycle and orchestration."""
    
    def __init__(self):
        """Initialize workflow manager."""
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def initialize(self):
        """Initialize connections."""
        print("Workflow manager initialized")
    
    async def shutdown(self):
        """Cleanup resources."""
        await self.client.aclose()
        print("Workflow manager shutdown")
    
    async def create_workflow(
        self,
        workflow_id: str,
        user_input: str,
        parameters: Dict[str, Any],
        metadata: Dict[str, Any],
    ) -> WorkflowStatus:
        """Create and start a new workflow."""
        now = datetime.utcnow()
        
        workflow_data = {
            "workflow_id": workflow_id,
            "user_input": user_input,
            "parameters": parameters,
            "metadata": metadata,
            "status": TaskStatus.PENDING,
            "current_stage": WorkflowStage.PARSING,
            "stages_completed": [],
            "progress_percentage": 0.0,
            "started_at": now,
            "updated_at": now,
            "results": {},
            "artifacts": [],
            "errors": [],
        }
        
        self.workflows[workflow_id] = workflow_data
        
        # Start workflow execution in background
        asyncio.create_task(self._execute_workflow(workflow_id))
        
        return WorkflowStatus(
            workflow_id=workflow_id,
            current_stage=WorkflowStage.PARSING,
            status=TaskStatus.PENDING,
            progress_percentage=0.0,
            stages_completed=[],
            started_at=now,
            updated_at=now,
        )
    
    async def _execute_workflow(self, workflow_id: str):
        """Execute workflow stages."""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return
        
        try:
            workflow["status"] = TaskStatus.RUNNING
            workflow["updated_at"] = datetime.utcnow()
            
            # Stage 1: NLP Parsing
            await self._execute_stage(workflow_id, WorkflowStage.PARSING)
            
            # Stage 2: Synthesis
            await self._execute_stage(workflow_id, WorkflowStage.SYNTHESIS)
            
            # Stage 3: RTL Generation
            await self._execute_stage(workflow_id, WorkflowStage.GENERATION)
            
            # Stage 4: Emulation
            await self._execute_stage(workflow_id, WorkflowStage.EMULATION)
            
            # Complete
            workflow["status"] = TaskStatus.COMPLETED
            workflow["current_stage"] = WorkflowStage.COMPLETE
            workflow["progress_percentage"] = 100.0
            workflow["updated_at"] = datetime.utcnow()
            
        except Exception as e:
            workflow["status"] = TaskStatus.FAILED
            workflow["errors"].append(str(e))
            workflow["updated_at"] = datetime.utcnow()
    
    async def _execute_stage(self, workflow_id: str, stage: WorkflowStage):
        """Execute a single workflow stage."""
        workflow = self.workflows[workflow_id]
        workflow["current_stage"] = stage
        workflow["updated_at"] = datetime.utcnow()
        
        stage_result = {"status": "completed", "timestamp": datetime.utcnow().isoformat()}
        
        try:
            if stage == WorkflowStage.PARSING:
                # Call NLP agent
                response = await self.client.post(
                    f"{settings.NLP_AGENT_URL}/parse",
                    json={"text": workflow["user_input"], "context": workflow["metadata"]}
                )
                response.raise_for_status()
                nlp_result = response.json()
                stage_result.update(nlp_result)
                # Store parsed entities for next stages
                workflow["parsed_spec"] = nlp_result.get("entities", {})
                workflow["constraints"] = nlp_result.get("constraints", {})
            
            elif stage == WorkflowStage.SYNTHESIS:
                # Call synthesis agent
                spec = workflow.get("parsed_spec", {})
                constraints = workflow.get("constraints", {})
                response = await self.client.post(
                    f"{settings.SYNTHESIS_AGENT_URL}/synthesize",
                    json={"spec": spec, "constraints": constraints}
                )
                response.raise_for_status()
                synth_result = response.json()
                stage_result.update(synth_result)
                # Store architecture for RTL generation
                workflow["architecture"] = synth_result.get("architecture", {})
            
            elif stage == WorkflowStage.GENERATION:
                # Call RTL generator
                architecture = workflow.get("architecture", {})
                response = await self.client.post(
                    f"{settings.RTL_GENERATOR_URL}/generate",
                    json={"spec": architecture, "language": "systemverilog"}
                )
                response.raise_for_status()
                rtl_result = response.json()
                stage_result.update(rtl_result)
                # Store RTL code for emulation
                workflow["rtl_code"] = rtl_result.get("code", "")
                workflow["module_name"] = rtl_result.get("module_name", "")
            
            elif stage == WorkflowStage.EMULATION:
                # Call emulator
                response = await self.client.post(
                    f"{settings.EMULATOR_URL}/emulate",
                    json={
                        "instructions": [],
                        "num_cycles": 100,
                        "config": {"module": workflow.get("module_name", "")}
                    }
                )
                response.raise_for_status()
                emu_result = response.json()
                stage_result.update(emu_result)
                # Collect artifacts
                if emu_result.get("waveform_data"):
                    workflow["artifacts"].append(emu_result["waveform_data"])
        
        except Exception as e:
            stage_result["error"] = str(e)
            stage_result["status"] = "failed"
            workflow["errors"].append(f"{stage}: {str(e)}")
        
        # Record stage completion
        workflow["stages_completed"].append(stage)
        
        # Update progress
        total_stages = 4
        workflow["progress_percentage"] = (len(workflow["stages_completed"]) / total_stages) * 100
        
        # Store stage result
        workflow["results"][stage] = stage_result
    
    async def get_workflow_status(self, workflow_id: str) -> Optional[WorkflowStatus]:
        """Get current workflow status."""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        
        return WorkflowStatus(
            workflow_id=workflow_id,
            current_stage=workflow["current_stage"],
            status=workflow["status"],
            progress_percentage=workflow["progress_percentage"],
            stages_completed=workflow["stages_completed"],
            started_at=workflow["started_at"],
            updated_at=workflow["updated_at"],
        )
    
    async def get_workflow_result(self, workflow_id: str) -> Optional[WorkflowResult]:
        """Get workflow result."""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return None
        
        execution_time = (workflow["updated_at"] - workflow["started_at"]).total_seconds() * 1000
        
        return WorkflowResult(
            workflow_id=workflow_id,
            status=workflow["status"],
            results=workflow["results"],
            artifacts=workflow["artifacts"],
            errors=workflow["errors"] if workflow["errors"] else None,
            execution_time_ms=execution_time,
            completed_at=workflow["updated_at"],
        )
    
    async def cancel_workflow(self, workflow_id: str) -> bool:
        """Cancel a running workflow."""
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            return False
        
        workflow["status"] = TaskStatus.CANCELLED
        workflow["updated_at"] = datetime.utcnow()
        return True

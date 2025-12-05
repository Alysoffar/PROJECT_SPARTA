"""Planning Agent - breaks down hardware design tasks into steps"""
from typing import Dict, Any, List


class PlanningAgent:
    """Agent that creates execution plans for hardware design tasks"""
    
    async def create_plan(self, user_message: str, context: List[Dict]) -> Dict[str, Any]:
        """
        Analyze user request and create step-by-step plan
        """
        message_lower = user_message.lower()
        
        steps = []
        
        # Determine design intent
        if any(word in message_lower for word in ["create", "design", "build", "generate"]):
            steps.append({
                "step": 1,
                "action": "parse_requirements",
                "description": "Extract hardware specifications from natural language"
            })
            steps.append({
                "step": 2,
                "action": "synthesize_architecture",
                "description": "Create high-level architecture and component breakdown"
            })
            steps.append({
                "step": 3,
                "action": "generate_rtl",
                "description": "Generate RTL/Verilog code"
            })
            steps.append({
                "step": 4,
                "action": "simulate",
                "description": "Run functional simulation and verify behavior"
            })
        
        elif any(word in message_lower for word in ["optimize", "improve", "refine"]):
            steps.append({
                "step": 1,
                "action": "load_previous_design",
                "description": "Retrieve existing design from memory"
            })
            steps.append({
                "step": 2,
                "action": "analyze_constraints",
                "description": "Identify optimization targets (area, power, timing)"
            })
            steps.append({
                "step": 3,
                "action": "re_synthesize",
                "description": "Apply optimization techniques"
            })
            steps.append({
                "step": 4,
                "action": "compare_metrics",
                "description": "Compare before/after metrics"
            })
        
        elif any(word in message_lower for word in ["simulate", "test", "verify"]):
            steps.append({
                "step": 1,
                "action": "load_design",
                "description": "Load RTL from context or memory"
            })
            steps.append({
                "step": 2,
                "action": "create_testbench",
                "description": "Generate test vectors"
            })
            steps.append({
                "step": 3,
                "action": "run_simulation",
                "description": "Execute simulation"
            })
            steps.append({
                "step": 4,
                "action": "analyze_results",
                "description": "Check for functional correctness"
            })
        
        else:
            # Default plan
            steps.append({
                "step": 1,
                "action": "clarify_intent",
                "description": "Understand user goal"
            })
            steps.append({
                "step": 2,
                "action": "execute_task",
                "description": "Perform requested action"
            })
        
        return {
            "intent": self._detect_intent(message_lower),
            "steps": steps,
            "estimated_time": len(steps) * 2,  # seconds
            "complexity": "simple" if len(steps) <= 3 else "moderate"
        }
    
    def _detect_intent(self, message: str) -> str:
        """Detect primary user intent"""
        if any(word in message for word in ["pcb", "board", "circuit board", "led matrix", "sensor board", "motor controller"]):
            return "pcb_design"
        elif any(word in message for word in ["create", "design", "build"]):
            return "design_creation"
        elif "optimize" in message or "improve" in message:
            return "optimization"
        elif "simulate" in message or "test" in message:
            return "verification"
        elif "explain" in message or "how" in message:
            return "explanation"
        else:
            return "general_query"

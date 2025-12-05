"""NLP Agent - parses hardware specifications from natural language"""
from typing import Dict, Any
import httpx


class NLPAgent:
    """Natural language processing for hardware design specs"""
    
    def __init__(self):
        self.nlp_service_url = "http://nlp-agent:8010"  # From docker-compose
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def parse(self, user_message: str, plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse user message into structured hardware specification
        Calls existing NLP microservice or runs inline parsing
        """
        try:
            # Try calling existing NLP service
            response = await self.client.post(
                f"{self.nlp_service_url}/parse",
                json={"text": user_message, "context": plan}
            )
            response.raise_for_status()
            result = response.json()
            return result
        except Exception:
            # Fallback to inline parsing if service unavailable
            return self._inline_parse(user_message)
    
    def _inline_parse(self, message: str) -> Dict[str, Any]:
        """Inline parsing when microservice unavailable"""
        message_lower = message.lower()
        
        spec = {
            "intent": "design_creation",
            "confidence": 0.85
        }
        
        # Component detection
        if "adder" in message_lower:
            spec["component"] = "adder"
            spec["bit_width"] = 4 if "4-bit" in message_lower or "4 bit" in message_lower else 8
            spec["description"] = "Arithmetic adder circuit"
        elif "alu" in message_lower:
            spec["component"] = "alu"
            spec["bit_width"] = 8 if "8-bit" in message_lower else 16
            spec["operations"] = ["ADD", "SUB", "AND", "OR", "XOR"]
            spec["description"] = "Arithmetic Logic Unit"
        elif "multiplier" in message_lower:
            spec["component"] = "multiplier"
            spec["bit_width"] = 8
            spec["description"] = "Integer multiplier"
        elif "fsm" in message_lower or "state machine" in message_lower:
            spec["component"] = "fsm"
            if "traffic" in message_lower:
                spec["states"] = ["RED", "YELLOW", "GREEN", "WALK"]
                spec["num_states"] = 4
                spec["description"] = "Traffic Light Controller FSM"
            elif "vending" in message_lower:
                spec["states"] = ["IDLE", "COIN_5", "COIN_10", "DISPENSE"]
                spec["num_states"] = 4
                spec["description"] = "Vending Machine FSM"
            else:
                spec["states"] = ["IDLE", "LOAD", "PROCESS", "DONE"]
                spec["num_states"] = 4
                spec["description"] = "Generic Finite State Machine"
        elif "uart" in message_lower:
            spec["component"] = "uart_tx"
            spec["baud_rate"] = 115200
            spec["data_bits"] = 8
            spec["stop_bits"] = 1
            spec["description"] = "UART Transmitter"
        elif "shift register" in message_lower or "shifter" in message_lower:
            spec["component"] = "shift_register"
            spec["bit_width"] = 8 if "8-bit" in message_lower else 4
            spec["shift_direction"] = "left" if "left" in message_lower else "right"
            spec["description"] = "Shift Register with Parallel Load"
        elif "counter" in message_lower:
            spec["component"] = "counter"
            spec["bit_width"] = 8 if "8-bit" in message_lower else 4
            spec["has_reset"] = "reset" in message_lower
            spec["has_enable"] = "enable" in message_lower
            spec["description"] = "Up Counter"
        elif "fifo" in message_lower or "buffer" in message_lower:
            spec["component"] = "fifo"
            spec["depth"] = 16
            spec["data_width"] = 8
            spec["description"] = "FIFO Buffer"
        else:
            spec["component"] = "generic_design"
            spec["description"] = "Custom hardware component"
        
        # Constraints
        spec["constraints"] = {}
        if "low power" in message_lower or "minimal area" in message_lower:
            spec["constraints"]["optimization_goal"] = "area"
        if "fast" in message_lower or "high performance" in message_lower:
            spec["constraints"]["optimization_goal"] = "speed"
        
        return spec
    
    async def refine_spec(self, spec: Dict[str, Any], error_message: str) -> Dict[str, Any]:
        """
        Refine specification based on error feedback (self-correction)
        """
        # Adjust bit widths if synthesis failed
        if "too large" in error_message.lower():
            if "bit_width" in spec:
                spec["bit_width"] = max(4, spec["bit_width"] // 2)
        
        # Simplify if complexity error
        if "complex" in error_message.lower():
            if "operations" in spec:
                spec["operations"] = spec["operations"][:3]  # Reduce operations
        
        return spec

"""Synthesis Agent - creates hardware architecture"""
from typing import Dict, Any
import httpx


class SynthesisAgent:
    """Hardware synthesis and architecture generation"""
    
    def __init__(self):
        self.synthesis_service_url = "http://synthesis-agent:8011"
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def synthesize(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Create hardware architecture from specification"""
        try:
            response = await self.client.post(
                f"{self.synthesis_service_url}/synthesize",
                json={"spec": spec, "constraints": spec.get("constraints", {})}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # Inline synthesis fallback
            return self._inline_synthesis(spec)
    
    def _inline_synthesis(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Inline synthesis when service unavailable"""
        component = spec.get("component", "generic")
        bit_width = spec.get("bit_width", 8)
        
        if component == "adder":
            return {
                "type": "ripple_carry_adder",
                "datapath_width": bit_width,
                "components": ["input_a", "input_b", "carry_chain", "sum", "carry_out"],
                "estimated_metrics": {
                    "area_mm2": 0.02 * bit_width,
                    "power_mw": 0.5 * bit_width,
                    "latency_ns": 2.0 + (0.3 * bit_width),
                    "lut_count": bit_width * 2
                }
            }
        elif component == "alu":
            return {
                "type": "arithmetic_logic_unit",
                "datapath_width": bit_width,
                "operations": spec.get("operations", ["ADD", "SUB", "AND", "OR", "XOR"]),
                "components": ["input_a", "input_b", "opcode_decoder", "adder", "logic_unit", "mux"],
                "estimated_metrics": {
                    "area_mm2": 0.08 * bit_width,
                    "power_mw": 2.5 * bit_width,
                    "latency_ns": 4.5,
                    "lut_count": bit_width * 6
                }
            }
        elif component == "fsm":
            num_states = spec.get("num_states", 4)
            states = spec.get("states", ["IDLE", "ACTIVE", "DONE"])
            return {
                "type": "finite_state_machine",
                "num_states": num_states,
                "state_names": states,
                "components": ["state_register", "next_state_logic", "output_logic"],
                "estimated_metrics": {
                    "area_mm2": 0.03 * num_states,
                    "power_mw": 0.8 * num_states,
                    "latency_ns": 2.5,
                    "lut_count": num_states * 4
                }
            }
        elif component == "uart_tx":
            return {
                "type": "uart_transmitter",
                "baud_rate": spec.get("baud_rate", 115200),
                "data_bits": spec.get("data_bits", 8),
                "components": ["shift_register", "baud_generator", "state_machine", "parity_logic"],
                "estimated_metrics": {
                    "area_mm2": 0.12,
                    "power_mw": 3.5,
                    "latency_ns": 8.0,
                    "lut_count": 32
                }
            }
        elif component == "counter":
            return {
                "type": "counter",
                "datapath_width": bit_width,
                "components": ["counter_register", "increment_logic", "reset_logic", "enable_logic"],
                "estimated_metrics": {
                    "area_mm2": 0.02 * bit_width,
                    "power_mw": 0.4 * bit_width,
                    "latency_ns": 2.2,
                    "lut_count": bit_width
                }
            }
        elif component == "shift_register":
            return {
                "type": "shift_register",
                "datapath_width": bit_width,
                "shift_direction": spec.get("shift_direction", "right"),
                "components": ["register_chain", "shift_control", "parallel_load"],
                "estimated_metrics": {
                    "area_mm2": 0.025 * bit_width,
                    "power_mw": 0.5 * bit_width,
                    "latency_ns": 1.8,
                    "lut_count": bit_width * 2
                }
            }
        else:
            return {
                "type": component,
                "datapath_width": bit_width,
                "components": ["input", "logic", "output"],
                "estimated_metrics": {
                    "area_mm2": 0.05,
                    "power_mw": 1.0,
                    "latency_ns": 3.0,
                    "lut_count": 10
                }
            }

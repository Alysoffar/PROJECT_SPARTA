"""NLP Agent main application."""
from typing import Dict, Any
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="SPARTA NLP Agent",
    version="0.1.0",
)


class ParseRequest(BaseModel):
    """Parse request model."""
    text: str
    context: Dict[str, Any] = {}


class ParseResult(BaseModel):
    """Parse result model."""
    intent: str
    entities: Dict[str, Any] = {}
    constraints: Dict[str, Any] = {}
    confidence: float = 0.0


@app.get("/health")
async def health_check():
    """Health check."""
    return {"service": "NLP Agent", "status": "healthy"}


@app.post("/parse", response_model=ParseResult)
async def parse_text(request: ParseRequest):
    """Parse natural language hardware specification."""
    # Simplified NLP parsing
    text_lower = request.text.lower()
    
    # Detect intent
    intent = "unknown"
    if "create" in text_lower or "design" in text_lower or "generate" in text_lower:
        intent = "design_creation"
    elif "optimize" in text_lower:
        intent = "optimization"
    elif "simulate" in text_lower or "emulate" in text_lower:
        intent = "simulation"
    
    # Extract entities (simplified)
    entities = {}
    if "adder" in text_lower:
        entities["component"] = "adder"
        entities["bit_width"] = 4 if "4-bit" in text_lower or "4 bit" in text_lower else 8
        entities["description"] = "Arithmetic adder circuit"
    elif "multiplier" in text_lower:
        entities["component"] = "multiplier"
        entities["bit_width"] = 8
        entities["description"] = "Integer multiplier"
    elif "alu" in text_lower:
        entities["component"] = "alu"
        entities["bit_width"] = 8 if "8-bit" in text_lower or "8 bit" in text_lower else 16
        entities["operations"] = ["ADD", "SUB", "AND", "OR", "XOR"]
        entities["description"] = "Arithmetic Logic Unit"
    elif "fsm" in text_lower or "state machine" in text_lower:
        entities["component"] = "fsm"
        entities["states"] = ["red", "green", "yellow"] if "traffic" in text_lower else ["idle", "active", "done"]
        entities["description"] = "Finite State Machine"
    elif "uart" in text_lower:
        entities["component"] = "uart_tx"
        entities["baud_rate"] = 115200
        entities["data_bits"] = 8
        entities["description"] = "UART Transmitter"
    else:
        entities["component"] = "generic_design"
        entities["description"] = "Custom hardware design"
    
    # Extract constraints
    constraints = {}
    if "low power" in text_lower or "minimal area" in text_lower:
        constraints["power"] = "low"
        constraints["optimization_goal"] = "area"
    if "high performance" in text_lower or "fast" in text_lower:
        constraints["performance"] = "high"
        constraints["optimization_goal"] = "speed"
    if "timing" in text_lower:
        constraints["timing_constraint_ns"] = 10.0
    
    return ParseResult(
        intent=intent,
        entities=entities,
        constraints=constraints,
        confidence=0.92,
    )

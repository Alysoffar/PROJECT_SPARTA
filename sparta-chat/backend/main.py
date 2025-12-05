"""
SPARTA Chat Backend - FastAPI Orchestrator
Multi-agent hardware design system with memory and self-correction
Supports: RTL design, PCB design, optimization, visualization
"""
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from agents.planning_agent import PlanningAgent
from agents.nlp_agent import NLPAgent
from agents.synthesis_agent import SynthesisAgent
from agents.rtl_agent import RTLAgent
from agents.emulation_agent import EmulationAgent
from agents.pcb_agent import PCBAgent
from agents.image_agent import ImageAgent
from memory.vector_memory import MemoryManager
from db.database import DatabaseManager
from utils.formatting import format_response, create_visualization
from utils.block_diagram import BlockDiagramGenerator
from utils.interactive_waveform import InteractiveWaveformGenerator
from utils.code_highlighter import CodeHighlighter
from api.downloads import save_session_design

app = FastAPI(title="SPARTA Chat Backend", version="2.0.0")

# Mount static files for generated images
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
memory_manager = MemoryManager()
db_manager = DatabaseManager()

# Initialize agents
planning_agent = PlanningAgent()
nlp_agent = NLPAgent()
synthesis_agent = SynthesisAgent()
rtl_agent = RTLAgent()
emulation_agent = EmulationAgent()
pcb_agent = PCBAgent()
image_agent = ImageAgent()

# Initialize utilities
block_diagram_gen = BlockDiagramGenerator()
waveform_gen = InteractiveWaveformGenerator()
code_highlighter = CodeHighlighter()


class ChatMessage(BaseModel):
    """Chat message model"""
    session_id: str
    message: str
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    session_id: str
    response: str
    visualization: Optional[str] = None
    block_diagram: Optional[str] = None
    interactive_waveform: Optional[str] = None
    highlighted_code: Optional[str] = None
    download_links: Optional[Dict[str, str]] = None
    metadata: Dict[str, Any]
    internal_notes: str


@app.on_event("startup")
async def startup():
    """Initialize database and memory on startup"""
    await db_manager.initialize()
    await memory_manager.initialize()
    print("✅ SPARTA Chat Backend initialized")


@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    await db_manager.close()
    print("👋 SPARTA Chat Backend shutdown")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SPARTA Chat Backend",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/search")
async def search_designs(query: str, limit: int = 5):
    """
    Search previous designs in memory
    """
    results = memory_manager.search(query, limit=limit)
    return {"query": query, "results": results}


@app.post("/generate_image")
async def generate_image_endpoint(request: dict):
    """
    Generate image from text prompt
    """
    prompt = request.get("prompt", "")
    context = request.get("context", {})
    
    result = await image_agent.generate_image(prompt, context)
    
    return {
        "status": result["status"],
        "image_path": result["image_path"],
        "model_used": result["model_used"],
        "prompt_used": result["prompt_used"]
    }


async def handle_pcb_design_quick(session_id: str, user_message: str, internal_notes: list):
    """Quick PCB design handler for better performance"""
    try:
        # Use PCB agent
        pcb_design = await pcb_agent.design_pcb({"purpose": user_message})
        
        # Format response
        response = f"""💬 **PCB Design Complete!**

**Purpose:** {user_message}

**Board Specifications:**
- Size: {pcb_design['board_size']['width']}mm x {pcb_design['board_size']['height']}mm
- Layers: {pcb_design['layers']}
- Components: {len(pcb_design['bom'])}

**Schematic Overview:**
```
{pcb_design['schematic'][:800]}
...
```

**Bill of Materials:**
{chr(10).join([f"- {item['component']}: {item['value']} ({item['package']}) - ${item['price']}" for item in pcb_design['bom'][:5]])}
{"..." if len(pcb_design['bom']) > 5 else ""}

✅ PCB design ready for manufacturing! Download Gerber files using the link below.
"""
        
        # Save to DB
        await db_manager.save_message(session_id, "assistant", response, {
            "type": "pcb",
            "component_count": len(pcb_design['bom']),
            "board_size": pcb_design['board_size']
        })
        
        # Save to memory
        await memory_manager.save_design(session_id, {
            "query": user_message,
            "pcb_design": pcb_design
        })
        
        # Save for downloads
        save_session_design(session_id, {"pcb_design": pcb_design})
        
        return ChatResponse(
            session_id=session_id,
            response=response,
            visualization=None,
            block_diagram=None,
            interactive_waveform=None,
            highlighted_code=None,
            download_links={
                "pcb_schematic": f"/download/pcb/schematic/{session_id}",
                "bom": f"/download/pcb/bom/{session_id}",
                "gerber": f"/download/pcb/gerber/{session_id}",
                "layout": f"/download/pcb/layout/{session_id}"
            },
            metadata={
                "type": "pcb",
                "component_count": len(pcb_design['bom']),
                "board_size": pcb_design['board_size']
            },
            internal_notes="\n".join(internal_notes)
        )
    except Exception as e:
        internal_notes.append(f"❌ PCB design error: {str(e)}")
        raise


@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Main chat endpoint - orchestrates multi-agent workflow with self-correction
    Optimized with parallel visualization generation
    """
    session_id = message.session_id
    user_message = message.message
    
    # Store user message in DB
    await db_manager.save_message(session_id, "user", user_message)
    
    # Load recent context from memory
    recent_context = await memory_manager.load_recent_messages(session_id, n=5)
    
    internal_notes = []
    attempts = 0
    max_attempts = 2  # Reduced from 3 to speed up
    success = False
    
    while not success and attempts < max_attempts:
        attempts += 1
        internal_notes.append(f"🔄 Attempt {attempts}/{max_attempts}")
        
        try:
            # Step 1: Planning agent breaks down the task
            plan = await planning_agent.create_plan(user_message, recent_context)
            internal_notes.append(f"✓ Plan: {len(plan.get('steps', []))} steps")
            
            # Detect PCB design first
            intent = plan.get("intent", "")
            if "pcb" in intent.lower() or any(kw in user_message.lower() for kw in ["pcb", "board", "circuit board"]):
                # Quick PCB design response
                return await handle_pcb_design_quick(session_id, user_message, internal_notes)
            
            # Step 2: NLP agent parses hardware requirements
            parsed_spec = await nlp_agent.parse(user_message, plan)
            internal_notes.append(f"✓ Parsed: {parsed_spec.get('component')}")
            
            # Step 3: Synthesis agent creates architecture
            architecture = await synthesis_agent.synthesize(parsed_spec)
            
            if architecture.get("error"):
                internal_notes.append(f"⚠️ Error, retrying...")
                continue
            
            # Generate diagram for EVERY design (always, in parallel with other work)
            internal_notes.append(f"🖼️ Generating diagram...")
            image_task = asyncio.create_task(
                image_agent.generate_image(
                    f"Technical diagram showing {parsed_spec.get('component', 'hardware design')}: {user_message}", 
                    {"plan": plan, "architecture": architecture, "spec": parsed_spec}
                )
            )
            
            # Step 4: RTL generation
            rtl_result = await rtl_agent.generate(architecture)
            
            if rtl_result.get("error"):
                internal_notes.append(f"⚠️ RTL error, retrying...")
                continue
            
            # Step 5: Simulation (lightweight)
            sim_result = await emulation_agent.simulate(rtl_result)
            
            if sim_result.get("error"):
                internal_notes.append(f"⚠️ Sim error, retrying...")
                continue
            
            internal_notes.append(f"✓ All stages completed!")
            success = True
            
            # Wait for image generation to complete
            try:
                image_result = await image_task
                if image_result["status"] in ["success", "fallback"]:
                    generated_image = image_result["image_path"]
                    internal_notes.append(f"✓ Diagram: {image_result['model_used']}")
                else:
                    generated_image = None
                    image_result = None
            except Exception as e:
                internal_notes.append(f"⚠️ Image generation failed: {e}")
                generated_image = None
                image_result = None
            
            # Format response
            response_text = format_response(
                parsed_spec=parsed_spec,
                architecture=architecture,
                rtl_code=rtl_result.get("code"),
                simulation=sim_result
            )
            
            # Add image to response (ALWAYS shown if generated)
            if generated_image and image_result:
                response_text = f"""**VISUAL DIAGRAM GENERATED**

![diagram]({generated_image})

**IMAGE GENERATION NOTES:**
- Model used: {image_result.get('model_used', 'matplotlib')}
- Status: {image_result.get('status', 'success').upper()}

---

{response_text}
"""
            
            # Generate visualizations in parallel (faster!)
            visualization, block_diagram = await asyncio.gather(
                create_visualization(sim_result.get("waveform_data", ""), session_id),
                block_diagram_gen.generate_diagram(architecture, parsed_spec),
                return_exceptions=True
            )
            
            # Handle exceptions from parallel tasks
            if isinstance(visualization, Exception):
                visualization = None
            if isinstance(block_diagram, Exception):
                block_diagram = None
            
            # Save design data for downloads
            save_session_design(session_id, {
                "rtl_code": rtl_result.get("code"),
                "testbench": rtl_result.get("testbench", ""),
                "parsed_spec": parsed_spec,
                "architecture": architecture,
                "simulation": sim_result
            })
            
            # Save to memory (async, don't wait)
            asyncio.create_task(memory_manager.save_design(session_id, {
                "query": user_message,
                "spec": parsed_spec,
                "architecture": architecture,
                "rtl": rtl_result.get("code"),
                "simulation": sim_result
            }))
            
            # Save to DB (async, don't wait)
            asyncio.create_task(db_manager.save_message(session_id, "assistant", response_text, {
                "plan": plan,
                "spec": parsed_spec,
                "metrics": architecture.get("estimated_metrics")
            }))
            
            return ChatResponse(
                session_id=session_id,
                response=response_text,
                visualization=visualization,
                block_diagram=block_diagram,
                interactive_waveform=None,  # Skip for speed
                highlighted_code=None,  # Skip for speed
                download_links={
                    "rtl_file": f"/download/rtl/{session_id}",
                    "testbench": f"/download/testbench/{session_id}",
                    "report": f"/download/report/{session_id}"
                },
                metadata={
                    "component": parsed_spec.get("component"),
                    "metrics": architecture.get("estimated_metrics"),
                    "simulation_status": sim_result.get("status"),
                    "attempts": attempts
                },
                internal_notes="\n".join(internal_notes)
            )
        
        except Exception as e:
            internal_notes.append(f"❌ Error: {str(e)}")
            if attempts >= max_attempts:
                # Final failure
                error_response = f"⚠️ Unable to complete design after {max_attempts} attempts.\n\nLast error: {str(e)}\n\nPlease try rephrasing your request or breaking it into smaller steps."
                await db_manager.save_message(session_id, "assistant", error_response, {"error": str(e)})
                
                return ChatResponse(
                    session_id=session_id,
                    response=error_response,
                    visualization=None,
                    metadata={"error": str(e), "attempts": attempts},
                    internal_notes="\n".join(internal_notes)
                )


@app.get("/history/{session_id}")
async def get_history(session_id: str, limit: int = 50):
    """Retrieve chat history for a session"""
    messages = await db_manager.get_messages(session_id, limit)
    return {"session_id": session_id, "messages": messages}


@app.get("/search")
async def search_memory(query: str, limit: int = 5):
    """Search memory for similar designs"""
    results = await memory_manager.search(query, limit)
    return {"query": query, "results": results}


# Include download endpoints
from api.downloads import router as download_router
app.include_router(download_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

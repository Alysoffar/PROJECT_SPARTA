"""
Enhanced chat endpoint with PCB design, block diagrams, interactive waveforms
This replaces the chat function in main.py
"""

async def enhanced_chat_endpoint(message: ChatMessage):
    """
    Enhanced chat endpoint supporting:
    - RTL hardware design
    - PCB board design
    - Interactive visualizations
    - Syntax highlighting
    - Download capabilities
    """
    session_id = message.session_id
    user_message = message.message
    
    # Store user message in DB
    await db_manager.save_message(session_id, "user", user_message)
    
    # Load recent context
    recent_context = await memory_manager.load_recent_messages(session_id, n=5)
    
    internal_notes = []
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        attempts += 1
        internal_notes.append(f"🔄 Attempt {attempts}/{max_attempts}")
        
        try:
            # Step 1: Planning
            plan = await planning_agent.create_plan(user_message, recent_context)
            intent = plan.get("intent")
            domain = plan.get("domain", "rtl")
            internal_notes.append(f"✓ Detected intent: {intent}, domain: {domain}")
            
            # Handle PCB design requests
            if domain == "pcb" or intent == "pcb_design":
                return await handle_pcb_design(session_id, user_message, internal_notes)
            
            # RTL Design flow
            parsed_spec = await nlp_agent.parse(user_message, plan)
            internal_notes.append(f"✓ Parsed: {parsed_spec.get('component')}")
            
            architecture = await synthesis_agent.synthesize(parsed_spec)
            if architecture.get("error"):
                internal_notes.append(f"⚠️ Synthesis error, retrying...")
                continue
            
            rtl_result = await rtl_agent.generate(architecture)
            if rtl_result.get("error"):
                internal_notes.append(f"⚠️ RTL error, retrying...")
                continue
            
            sim_result = await emulation_agent.simulate(rtl_result)
            if sim_result.get("error"):
                internal_notes.append(f"⚠️ Simulation error, retrying...")
                continue
            
            # Success! Generate all visualizations
            internal_notes.append("✅ Design complete, generating visualizations...")
            
            # 1. Format response
            response_text = format_response(parsed_spec, architecture, rtl_result.get("code"), sim_result)
            
            # 2. Static waveform
            visualization = await create_visualization(sim_result.get("waveform_data", ""), session_id)
            
            # 3. Block diagram
            block_diagram = await block_diagram_gen.generate_diagram(architecture, parsed_spec)
            
            # 4. Interactive waveform (Plotly)
            interactive_waveform = await waveform_gen.create_interactive_waveform(sim_result)
            
            # 5. Syntax highlighted code
            highlighted_code = code_highlighter.highlight_rtl(rtl_result.get("code", ""), "systemverilog")
            
            # 6. Code complexity analysis
            complexity = code_highlighter.get_complexity_score(rtl_result.get("code", ""))
            
            # 7. Create download links
            download_links = {
                "rtl_file": f"/download/rtl/{session_id}",
                "testbench": f"/download/testbench/{session_id}",
                "report": f"/download/report/{session_id}",
                "waveform_vcd": f"/download/vcd/{session_id}"
            }
            
            # Save to memory
            await memory_manager.save_design(session_id, {
                "query": user_message,
                "spec": parsed_spec,
                "architecture": architecture,
                "rtl": rtl_result.get("code"),
                "simulation": sim_result,
                "complexity": complexity
            })
            
            # Save to DB
            await db_manager.save_message(session_id, "assistant", response_text, {
                "plan": plan,
                "spec": parsed_spec,
                "metrics": architecture.get("estimated_metrics"),
                "complexity": complexity
            })
            
            return ChatResponse(
                session_id=session_id,
                response=response_text,
                visualization=visualization,
                block_diagram=block_diagram,
                interactive_waveform=interactive_waveform,
                highlighted_code=highlighted_code,
                download_links=download_links,
                metadata={
                    "component": parsed_spec.get("component"),
                    "metrics": architecture.get("estimated_metrics"),
                    "simulation_status": sim_result.get("status"),
                    "complexity": complexity,
                    "attempts": attempts,
                    "domain": domain
                },
                internal_notes="\\n".join(internal_notes)
            )
        
        except Exception as e:
            internal_notes.append(f"❌ Error: {str(e)}")
            if attempts >= max_attempts:
                error_msg = f"⚠️ Unable to complete design after {max_attempts} attempts.\\n\\nError: {str(e)}"
                await db_manager.save_message(session_id, "assistant", error_msg, {"error": str(e)})
                
                return ChatResponse(
                    session_id=session_id,
                    response=error_msg,
                    visualization=None,
                    block_diagram=None,
                    interactive_waveform=None,
                    highlighted_code=None,
                    download_links=None,
                    metadata={"error": str(e), "attempts": attempts},
                    internal_notes="\\n".join(internal_notes)
                )


async def handle_pcb_design(session_id: str, user_message: str, internal_notes: list):
    """Handle PCB design requests"""
    internal_notes.append("🔌 PCB design mode activated")
    
    # Parse PCB requirements
    requirements = {
        "purpose": user_message,
        "voltage": "5V",  # Default, should be parsed
        "components": []
    }
    
    # Generate PCB design
    pcb_design = await pcb_agent.design_pcb(requirements)
    
    # Format PCB response
    response_text = f"""💬 **PCB Design Complete!**

I've created your custom PCB design! Here's what I built:

**📋 Purpose:** {user_message}

**🔌 Board Specifications**
- Board Size: {pcb_design['board_size']['width']}mm x {pcb_design['board_size']['height']}mm
- Layers: {pcb_design['layers']}-layer board
- Trace Width: {pcb_design['trace_width']}
- Clearance: {pcb_design['clearance']}

**📐 Schematic**
```
{pcb_design['schematic']}
```

**📦 Bill of Materials (BOM)**
"""
    
    for item in pcb_design['bom']:
        response_text += f"- {item['ref']}: {item['value']} ({item['package']}) - Qty: {item['qty']} - ${item['price']}\\n"
    
    response_text += f"""

**🗺️ PCB Layout**
- Routing: {pcb_design['layout']['trace_routing']}
- Ground Plane: {pcb_design['layout']['ground_plane']}
- Via Count: {pcb_design['layout']['via_count']}
- Mounting Holes: {pcb_design['layout']['mounting_holes']}

**📁 Manufacturing Files (Gerber)**
"""
    
    for name, filename in pcb_design['gerber_files'].items():
        response_text += f"- {name.replace('_', ' ').title()}: `{filename}`\\n"
    
    response_text += """

✅ **Your PCB design is ready for manufacturing!**

💡 **Next Steps:**
- Review the schematic and BOM above
- Download Gerber files for manufacturing
- Send to PCB manufacturer (JLCPCB, PCBWay, etc.)
- Order components from the BOM
"""
    
    # Save design
    await memory_manager.save_design(session_id, {
        "query": user_message,
        "type": "pcb",
        "design": pcb_design
    })
    
    await db_manager.save_message(session_id, "assistant", response_text, {
        "type": "pcb",
        "board_size": pcb_design['board_size']
    })
    
    download_links = {
        "schematic": f"/download/pcb/schematic/{session_id}",
        "bom_csv": f"/download/pcb/bom/{session_id}",
        "gerber_zip": f"/download/pcb/gerber/{session_id}",
        "layout_pdf": f"/download/pcb/layout/{session_id}"
    }
    
    return ChatResponse(
        session_id=session_id,
        response=response_text,
        visualization=None,
        block_diagram=None,
        interactive_waveform=None,
        highlighted_code=None,
        download_links=download_links,
        metadata={
            "type": "pcb",
            "board_size": pcb_design['board_size'],
            "layers": pcb_design['layers'],
            "component_count": len(pcb_design['bom'])
        },
        internal_notes="\\n".join(internal_notes)
    )

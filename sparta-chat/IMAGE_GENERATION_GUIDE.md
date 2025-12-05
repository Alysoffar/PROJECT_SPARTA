# Image Generation Module - Feature Guide

## ✅ What Was Added

### 1. Image Generation Agent (`backend/agents/image_agent.py`)
- **Multi-model support**: OpenAI DALL-E, Replicate, Stable Diffusion, matplotlib fallback
- **Auto-detection**: Automatically chooses the best available model
- **Smart fallback**: Falls back to matplotlib diagrams if AI models fail
- **Specialized diagrams**: Architecture, flowchart, circuit, block diagrams

### 2. Backend Integration (`backend/main.py`)
- **Standalone endpoint**: `POST /generate_image`
- **Auto-detection in chat**: Detects image requests automatically
- **Static file serving**: `/static/generated/` for image files
- **Seamless integration**: Works with existing RTL/PCB workflows

### 3. Frontend Updates (`frontend/app.py`)
- **Image gallery**: Sidebar button to test image generation
- **Auto-display**: Images show automatically in chat
- **Fullscreen support**: Click images to view full size

## 🎯 How to Use

### Automatic Image Generation (in Chat)
Just ask naturally - the system detects when you want visuals:

```
User: "Show me the architecture of the system"
→ Generates architecture diagram automatically

User: "Draw a flowchart of the RTL generation process"
→ Creates flowchart

User: "Visualize the circuit schematic"
→ Generates circuit diagram

User: "I need a block diagram"
→ Creates block diagram
```

### Manual Image Generation (API)
```bash
curl -X POST http://localhost:9000/generate_image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "show the multi-agent architecture"}'
```

## 🔧 Trigger Keywords
The system automatically generates images when you use these words:
- diagram
- schematic  
- flowchart
- picture
- image
- architecture
- show me
- visualize
- draw

## 📊 Supported Diagram Types

### 1. Architecture Diagram
Shows multi-agent system layout with:
- Gateway
- All agents (Planning, NLP, Synthesis, RTL, Emulation, PCB, Image)
- Database and Memory connections
- Data flow arrows

### 2. Flowchart
Shows process flow with:
- User input → Planning → Parse → Synthesize → Generate → Simulate → Return
- Decision points
- Sequential steps

### 3. Circuit Schematic
Shows digital circuit with:
- Inputs/outputs
- Logic gates
- Flip-flops
- Connections

### 4. Block Diagram
Shows system blocks with:
- Input/output interfaces
- Controller
- Datapath
- Memory
- Connections

### 5. Generic Diagram
For any other request:
- Central concept
- Supporting elements in circular layout
- Connecting lines

## 🤖 Model Priority

1. **OpenAI DALL-E 3** (if `OPENAI_API_KEY` set)
   - Best quality
   - Most realistic
   - Requires API key

2. **Replicate SDXL** (if `REPLICATE_API_TOKEN` set)
   - Good quality
   - Cost-effective
   - Requires API key

3. **Local Stable Diffusion** (if running on `localhost:7860`)
   - Free
   - Private
   - Requires automatic1111 webui

4. **Matplotlib Fallback** (always available)
   - Fast
   - Free
   - Vector graphics
   - Technical diagrams only

## 🔄 Self-Correction Features

### Automatic Retry
- Tries 3 times with the selected model
- Switches models on failure
- Refines prompt based on error

### Prompt Sanitization
- Removes problematic characters
- Adds technical keywords
- Handles safety policy issues

### Fallback Chain
```
Primary Model Fail
  → Retry with refined prompt (3x)
    → Try next model
      → Matplotlib fallback (always succeeds)
```

## 📁 File Structure

```
backend/
  agents/
    image_agent.py          ← New image generation agent
  static/
    generated/              ← Generated images stored here
      matplotlib_*.png
      openai_*.png
      replicate_*.png
frontend/
  app.py                    ← Updated with image gallery
```

## 🎨 Response Format

When an image is generated, the chat response includes:

```markdown
💬 **Visual Diagram Generated!**

![diagram](static/generated/architecture_001.png)

🧠 **Image Generation Notes:**
- Model used: matplotlib_fallback
- Status: FALLBACK

---

[Rest of the normal response]
```

## 🚀 Examples

### Example 1: System Architecture
```
User: "Show me the SPARTA architecture"
Assistant: [Generates multi-agent architecture diagram]
```

### Example 2: Process Flow
```
User: "Draw a flowchart of how RTL is generated"
Assistant: [Creates flowchart with all steps]
```

### Example 3: Circuit Design
```
User: "Visualize a simple digital circuit"
Assistant: [Draws circuit schematic]
```

### Example 4: Block Diagram
```
User: "I need a block diagram of the datapath"
Assistant: [Creates block diagram]
```

## ⚙️ Configuration

### Enable OpenAI (Optional)
```bash
export OPENAI_API_KEY="sk-..."
```

### Enable Replicate (Optional)
```bash
export REPLICATE_API_TOKEN="r8_..."
```

### Enable Local SD (Optional)
1. Install automatic1111 webui
2. Start with: `python webui.py --api`
3. Access at `http://localhost:7860`

## 🎯 Integration Points

### In Chat Endpoint
```python
# Auto-detects image requests
needs_image = any(kw in user_message.lower() 
                  for kw in ["diagram", "schematic", ...])

if needs_image:
    image_result = await image_agent.generate_image(prompt, context)
```

### In Response
```python
if generated_image:
    response_text = f"""
💬 **Visual Diagram Generated!**
![diagram]({generated_image})
...
"""
```

## 📝 Notes

- Images are stored permanently in `static/generated/`
- Filenames include timestamp and counter for uniqueness
- All images are PNG format (150 DPI for matplotlib)
- Images can be downloaded via direct URL
- No cleanup - images persist for future reference

## ✅ Testing

Test the image generation:

1. **Via Chat UI**:
   - Type: "Show me the architecture"
   - Check for image in response

2. **Via API**:
   ```bash
   curl -X POST http://localhost:9000/generate_image \
     -H "Content-Type: application/json" \
     -d '{"prompt": "system architecture"}'
   ```

3. **Via Sidebar**:
   - Click "Generate Test Image" button
   - View in gallery

## 🎉 Complete!

The Image Generation Module is fully integrated and ready to use. The system will automatically generate diagrams whenever appropriate or when explicitly requested.

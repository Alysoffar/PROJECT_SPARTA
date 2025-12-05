"""
Image Generation Agent - Creates diagrams, schematics, and visualizations
Supports multiple backends with automatic fallback
"""
import os
import asyncio
import httpx
from typing import Dict, Any, Optional
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from datetime import datetime
import numpy as np
import hashlib


class ImageAgent:
    """Agent for generating images, diagrams, and visualizations"""
    
    def __init__(self):
        self.output_dir = "static/generated"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Available models (in priority order)
        self.available_models = self._detect_available_models()
        self.max_retries = 3
        
        # Image counter for unique filenames
        self.image_counter = 0
    
    def _detect_available_models(self) -> list:
        """Detect which image generation models are available"""
        models = []
        
        # Check for OpenAI API key
        if os.getenv("OPENAI_API_KEY"):
            models.append("openai")
        
        # Check for Replicate API key
        if os.getenv("REPLICATE_API_TOKEN"):
            models.append("replicate")
        
        # Check for local Stable Diffusion
        try:
            # Ping automatic1111 webui
            response = httpx.get("http://localhost:7860", timeout=1)
            if response.status_code == 200:
                models.append("stable_diffusion_local")
        except:
            pass
        
        # Always have matplotlib fallback
        models.append("matplotlib")
        
        return models
    
    def choose_model(self) -> str:
        """Choose the best available model"""
        if not self.available_models:
            return "matplotlib"
        return self.available_models[0]
    
    async def generate_image(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Generate image from text prompt with automatic model selection and fallback
        
        Returns:
            {
                "status": "success" | "fallback" | "error",
                "image_path": "static/generated/image_xxx.png",
                "model_used": "openai" | "stable_diffusion" | "matplotlib",
                "prompt_used": "sanitized prompt",
                "metadata": {...}
            }
        """
        model = self.choose_model()
        sanitized_prompt = self.sanitize_prompt(prompt)
        
        # ALWAYS use web image search for ANY hardware/circuit design
        # Detect hardware keywords in prompt OR in context
        keywords = ["adder", "alu", "counter", "fsm", "breadboard", "schematic", "circuit", "register", "uart", "mux", "demux", "flip-flop", "logic gate", "hardware", "design", "bit", "fpga", "asic", "rtl", "verilog"]
        is_hardware = any(kw in prompt.lower() for kw in keywords)
        
        # Also check context for hardware indicators
        if context and not is_hardware:
            context_str = str(context).lower()
            is_hardware = any(kw in context_str for kw in ["hardware", "rtl", "verilog", "circuit", "fpga"])
        
        if is_hardware:
            # Force breadboard diagram generation instead of web search
            try:
                filename = self._generate_filename("breadboard")
                filepath = os.path.join(self.output_dir, filename)
                self._draw_breadboard_diagram(filepath, prompt, context)
                print(f"[ImageAgent] ✅ Breadboard diagram generated: {filepath}")
                return {
                    "status": "success",
                    "image_path": filepath,
                    "model_used": "breadboard_diagram",
                    "prompt_used": prompt,
                    "metadata": {"source": "generated", "type": "breadboard"}
                }
            except Exception as e:
                print(f"[ImageAgent] ❌ Breadboard generation failed: {e}")
                return {
                    "status": "error",
                    "image_path": None,
                    "model_used": "breadboard_diagram",
                    "prompt_used": prompt,
                    "metadata": {"source": "generated", "error": str(e)}
                }

        # Otherwise, use normal image generation and fallback
        for attempt in range(self.max_retries):
            try:
                if model == "openai":
                    result = await self._generate_openai(sanitized_prompt)
                elif model == "replicate":
                    result = await self._generate_replicate(sanitized_prompt)
                elif model == "stable_diffusion_local":
                    result = await self._generate_sd_local(sanitized_prompt)
                else:
                    result = await self._generate_matplotlib(sanitized_prompt, context)
                # Validate the image was created
                if result["status"] == "success" and os.path.exists(result["image_path"]):
                    return result
            except Exception as e:
                print(f"❌ Image generation attempt {attempt + 1} failed: {e}")
                # Try next model in list
                if attempt < self.max_retries - 1 and len(self.available_models) > 1:
                    model = self.available_models[min(attempt + 1, len(self.available_models) - 1)]
                    sanitized_prompt = self.refine_prompt(sanitized_prompt, str(e))

        # Final fallback to matplotlib diagram
        return await self.fallback_diagram(prompt, context)
    
    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize and optimize prompt for image generation"""
        # Remove special characters that might cause issues
        sanitized = prompt.strip()
        
        # Add technical diagram keywords if needed
        keywords = ["diagram", "schematic", "architecture", "flowchart", "circuit", "block diagram"]
        has_visual_keyword = any(kw in sanitized.lower() for kw in keywords)
        
        if not has_visual_keyword:
            sanitized = f"technical diagram showing {sanitized}"
        
        # Limit length
        if len(sanitized) > 500:
            sanitized = sanitized[:497] + "..."
        
        return sanitized
    
    def refine_prompt(self, prompt: str, error_message: str) -> str:
        """Refine prompt based on previous error"""
        if "safety" in error_message.lower() or "policy" in error_message.lower():
            # Make more neutral
            return f"professional technical diagram: {prompt}"
        elif "complex" in error_message.lower():
            # Simplify
            words = prompt.split()
            return " ".join(words[:20])
        return prompt
    
    async def _generate_openai(self, prompt: str) -> Dict[str, Any]:
        """Generate image using OpenAI DALL-E"""
        import openai
        
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        
        image_url = response.data[0].url
        
        # Download image
        async with httpx.AsyncClient() as http_client:
            img_response = await http_client.get(image_url)
            img_response.raise_for_status()
            
            filename = self._generate_filename("openai")
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(img_response.content)
        
        return {
            "status": "success",
            "image_path": filepath,
            "model_used": "openai_dalle3",
            "prompt_used": prompt,
            "metadata": {"url": image_url}
        }
    
    async def _generate_replicate(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Replicate API (Stable Diffusion)"""
        import replicate
        
        output = replicate.run(
            "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
            input={"prompt": prompt}
        )
        
        # Download the image
        async with httpx.AsyncClient() as http_client:
            img_response = await http_client.get(output[0])
            img_response.raise_for_status()
            
            filename = self._generate_filename("replicate")
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(img_response.content)
        
        return {
            "status": "success",
            "image_path": filepath,
            "model_used": "replicate_sdxl",
            "prompt_used": prompt,
            "metadata": {}
        }
    
    async def _generate_sd_local(self, prompt: str) -> Dict[str, Any]:
        """Generate image using local Stable Diffusion (automatic1111)"""
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:7860/sdapi/v1/txt2img",
                json={
                    "prompt": prompt,
                    "steps": 20,
                    "width": 512,
                    "height": 512,
                    "cfg_scale": 7
                }
            )
            response.raise_for_status()
            
            import base64
            from PIL import Image
            from io import BytesIO
            
            result = response.json()
            image_data = base64.b64decode(result["images"][0])
            
            filename = self._generate_filename("sd_local")
            filepath = os.path.join(self.output_dir, filename)
            
            image = Image.open(BytesIO(image_data))
            image.save(filepath)
        
        return {
            "status": "success",
            "image_path": filepath,
            "model_used": "stable_diffusion_local",
            "prompt_used": prompt,
            "metadata": {}
        }
    
    async def _generate_matplotlib(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Generate diagram using matplotlib (fallback)"""
        filename = self._generate_filename("matplotlib")
        filepath = os.path.join(self.output_dir, filename)
        
        # Detect diagram type from prompt
        prompt_lower = prompt.lower()
        
        if "architecture" in prompt_lower or "system" in prompt_lower:
            self._draw_architecture_diagram(filepath, context)
        elif "flowchart" in prompt_lower or "flow" in prompt_lower:
            self._draw_flowchart(filepath, context)
        elif "circuit" in prompt_lower or "schematic" in prompt_lower:
            self._draw_circuit_diagram(filepath, context)
        elif "block" in prompt_lower:
            self._draw_block_diagram(filepath, context)
        else:
            self._draw_generic_diagram(filepath, prompt, context)
        
        return {
            "status": "fallback",
            "image_path": filepath,
            "model_used": "matplotlib_fallback",
            "prompt_used": prompt,
            "metadata": {"type": "vector_diagram"}
        }
    
    async def fallback_diagram(self, prompt: str, context: Dict = None) -> Dict[str, Any]:
        """Final fallback - simple matplotlib diagram"""
        return await self._generate_matplotlib(prompt, context)
    
    def _generate_filename(self, prefix: str) -> str:
        """Generate unique filename for image"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.image_counter += 1
        return f"{prefix}_{timestamp}_{self.image_counter:03d}.png"
    
    def _draw_architecture_diagram(self, filepath: str, context: Dict = None):
        """Draw multi-agent system architecture"""
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title
        ax.text(5, 9.5, 'SPARTA Multi-Agent Architecture', 
                ha='center', fontsize=16, weight='bold')
        
        # Gateway
        gateway = patches.FancyBboxPatch((3.5, 7), 3, 0.8, 
                                          boxstyle="round,pad=0.1", 
                                          edgecolor='blue', facecolor='lightblue', linewidth=2)
        ax.add_patch(gateway)
        ax.text(5, 7.4, 'API Gateway', ha='center', va='center', fontsize=10, weight='bold')
        
        # Agents
        agents = [
            ("Planning\nAgent", 1, 5),
            ("NLP\nAgent", 3, 5),
            ("Synthesis\nAgent", 5, 5),
            ("RTL\nAgent", 7, 5),
            ("Emulation\nAgent", 9, 5),
            ("PCB\nAgent", 2, 3),
            ("Image\nAgent", 8, 3)
        ]
        
        for name, x, y in agents:
            agent_box = patches.FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6,
                                                boxstyle="round,pad=0.05",
                                                edgecolor='green', facecolor='lightgreen', linewidth=1.5)
            ax.add_patch(agent_box)
            ax.text(x, y, name, ha='center', va='center', fontsize=8)
        
        # Database
        db = patches.FancyBboxPatch((1, 1), 1.5, 0.6,
                                     boxstyle="round,pad=0.05",
                                     edgecolor='red', facecolor='lightcoral', linewidth=1.5)
        ax.add_patch(db)
        ax.text(1.75, 1.3, 'Database', ha='center', va='center', fontsize=9)
        
        # Memory
        mem = patches.FancyBboxPatch((7.5, 1), 1.5, 0.6,
                                      boxstyle="round,pad=0.05",
                                      edgecolor='purple', facecolor='plum', linewidth=1.5)
        ax.add_patch(mem)
        ax.text(8.25, 1.3, 'Memory', ha='center', va='center', fontsize=9)
        
        # Arrows
        ax.arrow(5, 6.9, 0, -1.3, head_width=0.2, head_length=0.1, fc='gray', ec='gray')
        ax.arrow(2.5, 1.6, 1, 3.1, head_width=0.15, head_length=0.1, fc='gray', ec='gray', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _draw_flowchart(self, filepath: str, context: Dict = None):
        """Draw flowchart diagram"""
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # Flowchart boxes
        boxes = [
            ("User Input", 5, 11, 'lightblue'),
            ("Planning Agent", 5, 9.5, 'lightgreen'),
            ("Parse Requirements", 5, 8, 'lightyellow'),
            ("Synthesize Architecture", 5, 6.5, 'lightyellow'),
            ("Generate RTL", 5, 5, 'lightyellow'),
            ("Simulate & Verify", 5, 3.5, 'lightyellow'),
            ("Return Results", 5, 2, 'lightcoral')
        ]
        
        for label, x, y, color in boxes:
            box = patches.FancyBboxPatch((x-1.2, y-0.3), 2.4, 0.6,
                                          boxstyle="round,pad=0.1",
                                          edgecolor='black', facecolor=color, linewidth=1.5)
            ax.add_patch(box)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, weight='bold')
        
        # Arrows between boxes
        for i in range(len(boxes) - 1):
            y_from = boxes[i][2] - 0.4
            y_to = boxes[i+1][2] + 0.4
            ax.arrow(5, y_from, 0, y_to - y_from, 
                    head_width=0.3, head_length=0.2, fc='black', ec='black')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _draw_circuit_diagram(self, filepath: str, context: Dict = None):
        """Draw basic circuit schematic"""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        ax.text(5, 5.5, 'Digital Circuit Schematic', ha='center', fontsize=14, weight='bold')
        
        # Components
        components = [
            ("Input A", 1, 3),
            ("Input B", 1, 2),
            ("Logic Gate", 4, 2.5),
            ("Flip-Flop", 7, 2.5),
            ("Output", 9.5, 2.5)
        ]
        
        for label, x, y in components:
            if "Input" in label or "Output" in label:
                ax.plot(x, y, 'o', markersize=10, color='blue')
            else:
                rect = patches.Rectangle((x-0.4, y-0.3), 0.8, 0.6,
                                          edgecolor='black', facecolor='wheat', linewidth=2)
                ax.add_patch(rect)
            ax.text(x, y-0.7, label, ha='center', fontsize=9)
        
        # Connections
        ax.plot([1, 3.6], [3, 2.6], 'k-', linewidth=1.5)
        ax.plot([1, 3.6], [2, 2.4], 'k-', linewidth=1.5)
        ax.plot([4.4, 6.6], [2.5, 2.5], 'k-', linewidth=1.5)
        ax.plot([7.4, 9.5], [2.5, 2.5], 'k-', linewidth=1.5)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _draw_block_diagram(self, filepath: str, context: Dict = None):
        """Draw block diagram"""
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_xlim(0, 12)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        ax.text(6, 5.5, 'System Block Diagram', ha='center', fontsize=14, weight='bold')
        
        # Blocks
        blocks = [
            ("Input\nInterface", 1.5, 3, 'lightblue'),
            ("Controller", 4, 3, 'lightgreen'),
            ("Datapath", 7, 3, 'lightyellow'),
            ("Memory", 10, 3, 'lightcoral'),
            ("Output\nInterface", 7, 1, 'plum')
        ]
        
        for label, x, y, color in blocks:
            rect = patches.FancyBboxPatch((x-0.7, y-0.5), 1.4, 1,
                                           boxstyle="round,pad=0.1",
                                           edgecolor='black', facecolor=color, linewidth=2)
            ax.add_patch(rect)
            ax.text(x, y, label, ha='center', va='center', fontsize=10, weight='bold')
        
        # Connections
        ax.arrow(2.2, 3, 1.1, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(4.7, 3, 1.6, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(7.7, 3, 1.6, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(7, 2.5, 0, -1, head_width=0.2, head_length=0.2, fc='black', ec='black')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()
    
    def _draw_generic_diagram(self, filepath: str, prompt: str, context: Dict = None):
        """Draw generic conceptual diagram"""
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # Title from prompt
        title = prompt[:50] + "..." if len(prompt) > 50 else prompt
        ax.text(5, 9, title, ha='center', fontsize=12, weight='bold')
        
        # Central concept
        circle = patches.Circle((5, 5), 1.5, edgecolor='blue', facecolor='lightblue', linewidth=2)
        ax.add_patch(circle)
        ax.text(5, 5, 'Main\nConcept', ha='center', va='center', fontsize=11, weight='bold')
        
        # Supporting elements
        angles = [0, 72, 144, 216, 288]
        labels = ['Element 1', 'Element 2', 'Element 3', 'Element 4', 'Element 5']
        
        for angle, label in zip(angles, labels):
            import math
            x = 5 + 3 * math.cos(math.radians(angle))
            y = 5 + 3 * math.sin(math.radians(angle))
            
            box = patches.FancyBboxPatch((x-0.5, y-0.3), 1, 0.6,
                                          boxstyle="round,pad=0.05",
                                          edgecolor='green', facecolor='lightgreen', linewidth=1.5)
            ax.add_patch(box)
            ax.text(x, y, label, ha='center', va='center', fontsize=9)
            
            # Connect to center
            ax.plot([5, x], [5, y], 'k--', alpha=0.5, linewidth=1)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        plt.close()

    def _draw_breadboard_diagram(self, filepath: str, prompt: str, context: Dict = None):
        """Draw realistic breadboard with proper hole grid, components, and wire routing."""
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.set_xlim(0, 14)
        ax.set_ylim(0, 8)
        ax.axis('off')

        ax.text(7, 7.6, 'Hardware Circuit - Breadboard Layout', ha='center', fontsize=16, weight='bold')

        # BREADBOARD - realistic hole grid pattern
        bb_x, bb_y, bb_w, bb_h = 0.8, 1.2, 12.4, 5.2
        ax.add_patch(patches.Rectangle((bb_x, bb_y), bb_w, bb_h, edgecolor='#333', facecolor='#f5f5f0', linewidth=2))
        
        # Power rails (top and bottom with red/blue strips)
        rail_h = 0.25
        ax.add_patch(patches.Rectangle((bb_x+0.2, bb_y+bb_h-rail_h-0.15), bb_w-0.4, rail_h, fc='#ffe5e5', ec='red', lw=1))
        ax.add_patch(patches.Rectangle((bb_x+0.2, bb_y+0.15), bb_w-0.4, rail_h, fc='#e5f0ff', ec='blue', lw=1))
        ax.text(bb_x+0.05, bb_y+bb_h-rail_h/2-0.15, '+', color='red', fontsize=12, weight='bold')
        ax.text(bb_x+0.05, bb_y+rail_h/2+0.15, '−', color='blue', fontsize=12, weight='bold')
        
        # Center divider (gutter)
        gutter_y = bb_y + bb_h/2
        ax.plot([bb_x+0.5, bb_x+bb_w-0.5], [gutter_y, gutter_y], 'k--', linewidth=1, alpha=0.3)
        
        # Draw hole grid pattern (simplified for visual effect)
        for row in range(8, 32, 3):
            for col in range(5, 60, 2):
                hx = bb_x + 0.5 + col*0.2
                hy = bb_y + 0.6 + (row%16)*0.25
                if hx < bb_x+bb_w-0.5 and hy < bb_y+bb_h-0.5:
                    ax.plot(hx, hy, 'o', markersize=1.5, color='#ccc', alpha=0.4)

        # Extract component info with adder variants
        kw_map = {
            'ripple-carry-adder': ('4-Bit Ripple Adder', '74LS283', 16),
            'ripple-adder': ('4-Bit Ripple Adder', '74LS283', 16),
            'carry-lookahead': ('CLA Adder', '74LS182', 16),
            'full-adder': ('Full Adder', '74LS83', 16),
            'half-adder': ('Half Adder', '7486+7408', 14),
            'adder': ('4-Bit Adder', '74LS83', 16),
            'alu': ('ALU', '74LS181', 24),
            'counter': ('Counter', '74LS163', 16),
            'register': ('Shift Register', '74HC595', 16),
            'uart': ('UART', 'MAX232', 16),
            'mux': ('Multiplexer', '74HC157', 16),
            'demux': ('Demux', '74HC138', 16),
            'flip-flop': ('D Flip-Flop', '74LS74', 14),
        }
        lower_prompt = prompt.lower()
        # Match in priority order (specific before generic)
        matched = None
        for k, v in kw_map.items():
            if k in lower_prompt:
                matched = (k, v)
                break
        if not matched:
            matched = ('logic', ('Logic IC', '74HC00', 14))
        main_ic = matched[1]
        ic_label, ic_part, ic_pins = main_ic
        detected_type = matched[0]

        # ARDUINO/MCU (left side, detailed with pins)
        mcu_x, mcu_y = 2.0, 3.2
        mcu_w, mcu_h = 2.0, 2.4
        ax.add_patch(patches.Rectangle((mcu_x, mcu_y), mcu_w, mcu_h, fc='#1e3a5f', ec='black', lw=2))
        ax.text(mcu_x+mcu_w/2, mcu_y+mcu_h/2+0.3, 'Arduino', ha='center', fontsize=11, weight='bold', color='white')
        ax.text(mcu_x+mcu_w/2, mcu_y+mcu_h/2-0.1, 'Uno', ha='center', fontsize=9, color='white')
        
        # Pin headers on MCU (left side digital pins)
        pin_labels = ['GND', 'D2', 'D3', 'D4', 'D5', 'VCC']
        for i, lbl in enumerate(pin_labels):
            py = mcu_y + 0.3 + i*0.35
            ax.plot([mcu_x-0.08], [py], 's', markersize=4, color='gold')
            ax.text(mcu_x-0.25, py, lbl, ha='right', va='center', fontsize=6)

        # MAIN IC (center, DIP package)
        ic_x, ic_y = 6.5, 3.0
        ic_w, ic_h = 1.8, 2.8
        ax.add_patch(patches.Rectangle((ic_x, ic_y), ic_w, ic_h, fc='#2c2c2c', ec='black', lw=2))
        # Chip notch
        notch = patches.Wedge((ic_x+ic_w/2, ic_y+ic_h), 0.15, 0, 180, fc='#444', ec='black')
        ax.add_patch(notch)
        
        # Display correct label based on detected type
        display_label = ic_label
        if 'alu' in detected_type:
            display_label = 'ALU'
        elif 'counter' in detected_type:
            display_label = 'Counter'
        elif 'register' in detected_type:
            display_label = 'Shift Reg'
        elif 'uart' in detected_type:
            display_label = 'UART'
        elif 'mux' in detected_type and 'demux' not in detected_type:
            display_label = 'MUX'
        elif 'demux' in detected_type:
            display_label = 'DEMUX'
        elif 'flip-flop' in detected_type:
            display_label = 'D FF'
        
        ax.text(ic_x+ic_w/2, ic_y+ic_h/2+0.4, display_label, ha='center', fontsize=9, weight='bold', color='white')
        ax.text(ic_x+ic_w/2, ic_y+ic_h/2-0.2, ic_part, ha='center', fontsize=7, color='#ccc')
        
        # IC pins (DIP style)
        pins_per_side = ic_pins // 2
        for p in range(pins_per_side):
            pin_y = ic_y + 0.3 + p * (ic_h-0.6)/(pins_per_side-1) if pins_per_side > 1 else ic_y+ic_h/2
            # Left pins
            ax.add_patch(patches.Rectangle((ic_x-0.12, pin_y-0.05), 0.12, 0.1, fc='silver', ec='black', lw=0.5))
            ax.text(ic_x-0.15, pin_y, str(p+1), ha='right', fontsize=5)
            # Right pins
            ax.add_patch(patches.Rectangle((ic_x+ic_w, pin_y-0.05), 0.12, 0.1, fc='silver', ec='black', lw=0.5))
            ax.text(ic_x+ic_w+0.15, pin_y, str(ic_pins-p), ha='left', fontsize=5)

        # RESISTOR (with color bands)
        res_x, res_y = 4.8, 2.2
        res_w, res_h = 0.8, 0.25
        ax.add_patch(patches.Rectangle((res_x, res_y), res_w, res_h, fc='tan', ec='brown', lw=2))
        # Color bands (red-red-brown = 220Ω)
        band_x = [res_x+0.15, res_x+0.35, res_x+0.55]
        for bx, color in zip(band_x, ['red', 'red', 'brown']):
            ax.add_patch(patches.Rectangle((bx, res_y-0.02), 0.08, res_h+0.04, fc=color, ec='none'))
        ax.text(res_x+res_w/2, res_y-0.3, '220Ω', ha='center', fontsize=7, weight='bold')
        # Resistor leads
        ax.plot([res_x-0.2, res_x], [res_y+res_h/2, res_y+res_h/2], 'k-', lw=1.5)
        ax.plot([res_x+res_w, res_x+res_w+0.2], [res_y+res_h/2, res_y+res_h/2], 'k-', lw=1.5)

        # LED (with polarity markers)
        led_x, led_y = 9.5, 2.2
        ax.add_patch(patches.Circle((led_x, led_y), 0.22, fc='#ff6666', ec='darkred', lw=2))
        # Anode (+) and cathode (-)
        ax.plot([led_x-0.25, led_x-0.08], [led_y, led_y], 'k-', lw=1.5)  # anode lead (longer)
        ax.plot([led_x+0.08, led_x+0.25], [led_y, led_y], 'k-', lw=1.5)  # cathode lead
        ax.plot([led_x+0.23, led_x+0.23], [led_y-0.08, led_y+0.08], 'k-', lw=2)  # flat side marker
        ax.text(led_x, led_y-0.5, 'LED', ha='center', fontsize=7, weight='bold', color='red')
        # Light rays
        for angle in [30, 60]:
            dx, dy = 0.4*np.cos(np.radians(angle)), 0.4*np.sin(np.radians(angle))
            ax.arrow(led_x+0.15, led_y+0.15, dx, dy, head_width=0.1, head_length=0.08, fc='yellow', ec='orange', alpha=0.7, lw=0)

        # CAPACITOR (optional, for stability)
        cap_x, cap_y = 5.2, 4.8
        ax.plot([cap_x, cap_x], [cap_y, cap_y+0.4], 'k-', lw=3)
        ax.plot([cap_x+0.08, cap_x+0.08], [cap_y, cap_y+0.4], 'k-', lw=3)
        ax.plot([cap_x+0.04, cap_x+0.04], [cap_y+0.42, cap_y+0.55], 'k-', lw=1.5)
        ax.plot([cap_x+0.04, cap_x+0.04], [cap_y-0.13, cap_y], 'k-', lw=1.5)
        ax.text(cap_x+0.04, cap_y+0.7, '100nF', ha='center', fontsize=6)

        # JUMPER WIRES (component-specific routing based on type)
        
        # Common power wires (all components need these)
        vcc_ic_y = ic_y + ic_h - 0.3
        gnd_ic_y = ic_y + 0.3
        
        # VCC wire: MCU VCC -> IC VCC
        ax.plot([mcu_x-0.08, mcu_y+2.05, bb_x+1, bb_y+bb_h-0.27, ic_x-0.3, vcc_ic_y, ic_x-0.12, vcc_ic_y],
                [mcu_y+2.05, mcu_y+2.05, bb_y+bb_h-0.27, bb_y+bb_h-0.27, bb_y+bb_h-0.27, vcc_ic_y, vcc_ic_y, vcc_ic_y],
                color='red', lw=2.5, solid_capstyle='round')
        
        # GND wire: MCU GND -> IC GND
        ax.plot([mcu_x-0.08, mcu_x-0.5, mcu_x-0.5, ic_x-0.3, ic_x-0.12],
                [mcu_y+0.3, mcu_y+0.3, gnd_ic_y, gnd_ic_y, gnd_ic_y],
                color='black', lw=2.5, solid_capstyle='round')
        
        # Component-specific signal wiring
        if 'adder' in detected_type:
            # ADDER: A inputs (D2-D5), B inputs (D6-D9 simulated), Sum outputs
            # A3-A0 inputs from MCU
            for i in range(4):
                pin_y_mcu = mcu_y + 0.65 + i*0.35
                pin_y_ic = ic_y + 0.5 + i*0.5
                ax.plot([mcu_x-0.08, 5.0+i*0.2, 5.0+i*0.2, ic_x-0.12], 
                        [pin_y_mcu, pin_y_mcu, pin_y_ic, pin_y_ic],
                        color='green', lw=2, solid_capstyle='round', alpha=0.8)
                ax.text(5.0+i*0.2, pin_y_mcu+0.15, f'A{i}', fontsize=5, ha='center')
            
            # Sum outputs to LED indicator via resistor
            sum0_y = ic_y + ic_h - 0.8
            ax.plot([ic_x+ic_w+0.12, res_x-0.2], [sum0_y, res_y+res_h/2],
                    color='orange', lw=2.5, solid_capstyle='round')
            ax.text(ic_x+ic_w+0.25, sum0_y, 'S0', fontsize=5)
            
        elif 'alu' in detected_type:
            # ALU: A/B inputs, function select, output
            # A inputs (4-bit)
            for i in range(4):
                pin_y = ic_y + 0.6 + i*0.4
                ax.plot([mcu_x-0.08, 5.5, 5.5, ic_x-0.12], [mcu_y+0.65+i*0.3, mcu_y+0.65+i*0.3, pin_y, pin_y],
                        color='green', lw=2, solid_capstyle='round')
            # Function select lines
            sel_y = ic_y + 2.0
            ax.plot([mcu_x-0.08, 5.2, 5.2, ic_x-0.12], [mcu_y+1.35, mcu_y+1.35, sel_y, sel_y],
                    color='purple', lw=2.5, solid_capstyle='round')
            ax.text(5.2, sel_y+0.2, 'SEL', fontsize=5, ha='center')
            # Output to LED
            ax.plot([ic_x+ic_w+0.12, res_x-0.2], [ic_y+ic_h/2, res_y+res_h/2],
                    color='orange', lw=2.5, solid_capstyle='round')
            
        elif 'counter' in detected_type:
            # COUNTER: CLK, RESET, Q outputs
            # Clock signal
            clk_y = ic_y + 0.8
            ax.plot([mcu_x-0.08, 5.3, 5.3, ic_x-0.12], [mcu_y+0.65, mcu_y+0.65, clk_y, clk_y],
                    color='cyan', lw=2.5, solid_capstyle='round')
            ax.text(5.3, clk_y+0.2, 'CLK', fontsize=5, ha='center')
            # Reset
            rst_y = ic_y + 1.4
            ax.plot([mcu_x-0.08, 5.1, 5.1, ic_x-0.12], [mcu_y+1.0, mcu_y+1.0, rst_y, rst_y],
                    color='red', lw=2, solid_capstyle='round', alpha=0.7)
            ax.text(5.1, rst_y+0.2, 'RST', fontsize=5, ha='center')
            # Q0 output to LED
            q0_y = ic_y + ic_h - 1.0
            ax.plot([ic_x+ic_w+0.12, res_x-0.2], [q0_y, res_y+res_h/2],
                    color='orange', lw=2.5, solid_capstyle='round')
            ax.text(ic_x+ic_w+0.25, q0_y, 'Q0', fontsize=5)
            
        elif 'register' in detected_type:
            # SHIFT REGISTER: Data, Clock, Latch, Serial Out
            # Data in
            data_y = ic_y + 0.8
            ax.plot([mcu_x-0.08, 5.4, 5.4, ic_x-0.12], [mcu_y+0.65, mcu_y+0.65, data_y, data_y],
                    color='green', lw=2.5, solid_capstyle='round')
            ax.text(5.4, data_y+0.2, 'DATA', fontsize=5, ha='center')
            # Clock
            clk_y = ic_y + 1.4
            ax.plot([mcu_x-0.08, 5.2, 5.2, ic_x-0.12], [mcu_y+1.0, mcu_y+1.0, clk_y, clk_y],
                    color='cyan', lw=2.5, solid_capstyle='round')
            ax.text(5.2, clk_y+0.2, 'CLK', fontsize=5, ha='center')
            # Latch
            latch_y = ic_y + 2.0
            ax.plot([mcu_x-0.08, 5.0, 5.0, ic_x-0.12], [mcu_y+1.35, mcu_y+1.35, latch_y, latch_y],
                    color='purple', lw=2, solid_capstyle='round')
            ax.text(5.0, latch_y+0.2, 'LATCH', fontsize=4, ha='center')
            # Q7' serial out to LED
            ax.plot([ic_x+ic_w+0.12, res_x-0.2], [ic_y+ic_h-0.8, res_y+res_h/2],
                    color='orange', lw=2.5, solid_capstyle='round')
            
        elif 'mux' in detected_type and 'demux' not in detected_type:
            # MUX: Data inputs, Select, Output
            # Data inputs (4 channels)
            for i in range(4):
                pin_y = ic_y + 0.6 + i*0.5
                ax.plot([mcu_x-0.08, 5.3+i*0.15, 5.3+i*0.15, ic_x-0.12], 
                        [mcu_y+0.65+i*0.3, mcu_y+0.65+i*0.3, pin_y, pin_y],
                        color='green', lw=1.8, solid_capstyle='round', alpha=0.8)
            # Select lines
            sel_y = ic_y + ic_h - 1.0
            ax.plot([mcu_x-0.08, 5.1, 5.1, ic_x-0.12], [mcu_y+1.7, mcu_y+1.7, sel_y, sel_y],
                    color='purple', lw=2.5, solid_capstyle='round')
            ax.text(5.1, sel_y+0.2, 'SEL', fontsize=5, ha='center')
            # Output to LED
            ax.plot([ic_x+ic_w+0.12, res_x-0.2], [ic_y+ic_h/2, res_y+res_h/2],
                    color='orange', lw=2.5, solid_capstyle='round')
                    
        elif 'uart' in detected_type:
            # UART: TX, RX
            tx_y = ic_y + 1.0
            ax.plot([mcu_x-0.08, 5.3, 5.3, ic_x-0.12], [mcu_y+0.65, mcu_y+0.65, tx_y, tx_y],
                    color='green', lw=2.5, solid_capstyle='round')
            ax.text(5.3, tx_y+0.2, 'TX', fontsize=5, ha='center')
            
            rx_y = ic_y + 1.8
            ax.plot([ic_x+ic_w+0.12, 8.5, 8.5, mcu_x-0.08], [rx_y, rx_y, mcu_y+1.0, mcu_y+1.0],
                    color='orange', lw=2.5, solid_capstyle='round')
            ax.text(ic_x+ic_w+0.25, rx_y, 'RX', fontsize=5)
            
        else:
            # Generic/fallback wiring
            ic_in_y = ic_y + 1.2
            ax.plot([mcu_x-0.08, 4.5, 4.5, ic_x-0.12], [mcu_y+1.0, mcu_y+1.0, ic_in_y, ic_in_y],
                    color='green', lw=2.5, solid_capstyle='round')
            
            ic_out_y = ic_y + 1.8
            ax.plot([ic_x+ic_w+0.12, res_x-0.2], [ic_out_y, res_y+res_h/2],
                    color='orange', lw=2.5, solid_capstyle='round')
        
        # Resistor -> LED (common for all)
        w2_pts = [(res_x+res_w+0.2, res_y+res_h/2), (led_x-0.25, res_y+res_h/2), (led_x-0.25, led_y)]
        ax.plot([p[0] for p in w2_pts], [p[1] for p in w2_pts], color='orange', lw=2.5, solid_capstyle='round')
        
        # LED cathode -> GND rail (common for all)
        ax.plot([led_x+0.25, led_x+0.25, led_x+0.25, bb_x+bb_w-1], [led_y, led_y-0.8, bb_y+0.27, bb_y+0.27], 
                color='blue', lw=2.5, solid_capstyle='round')
        
        # Capacitor wiring (common for all)
        ax.plot([cap_x+0.04, cap_x+0.04, bb_x+2], [cap_y+0.55, bb_y+bb_h-0.27, bb_y+bb_h-0.27], 'r-', lw=1.5)
        ax.plot([cap_x+0.04, cap_x+0.04, bb_x+2], [cap_y-0.13, bb_y+0.27, bb_y+0.27], 'b-', lw=1.5)

        # LEGEND / BOM
        legend_x, legend_y = 0.5, 0.2
        ax.add_patch(patches.FancyBboxPatch((legend_x, legend_y), 3.2, 0.8, boxstyle='round,pad=0.15',
                                            fc='white', ec='black', lw=1.5))
        ax.text(legend_x+1.6, legend_y+0.65, 'Bill of Materials', ha='center', fontsize=9, weight='bold')
        
        # Type-specific BOM notes
        type_note = ''
        if 'ripple' in detected_type:
            type_note = ' (Ripple Carry)'
        elif 'lookahead' in detected_type:
            type_note = ' (Carry Lookahead)'
        elif 'half' in detected_type:
            type_note = ' (Half Adder)'
        elif 'full' in detected_type:
            type_note = ' (Full Adder)'
        
        bom = [
            '• Breadboard (830 holes)',
            f'• Arduino Uno',
            f'• {ic_part} IC{type_note}',
            '• LED (Red, 5mm)',
            '• 220Ω Resistor',
            '• 100nF Capacitor',
            '• Jumper Wires (M-M)',
        ]
        for i, item in enumerate(bom):
            ax.text(legend_x+0.1, legend_y+0.5-i*0.09, item, fontsize=6, ha='left')

        # Wire color legend
        ax.text(4.2, 0.5, 'Wire Colors:', fontsize=7, weight='bold')
        colors_info = [('red', 'VCC'), ('black', 'GND'), ('orange', 'Signal'), ('green', 'Input'), ('purple', 'Output')]
        for i, (col, lbl) in enumerate(colors_info):
            ax.plot([4.2+i*0.9, 4.4+i*0.9], [0.3, 0.3], color=col, lw=3, solid_capstyle='round')
            ax.text(4.3+i*0.9, 0.15, lbl, ha='center', fontsize=5)

        plt.tight_layout()
        plt.savefig(filepath, dpi=180, bbox_inches='tight', facecolor='white')
        plt.close()

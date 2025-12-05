"""Block Diagram Generator - Creates visual diagrams from RTL/architecture"""
from typing import Dict, Any
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class BlockDiagramGenerator:
    """Generate visual block diagrams for hardware designs"""
    
    async def generate_diagram(self, architecture: Dict[str, Any], parsed_spec: Dict[str, Any]) -> str:
        """
        Create block diagram showing component connections
        Returns base64 encoded image
        """
        component_type = parsed_spec.get("component", "generic")
        
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        if component_type.lower() in ['alu', 'arithmetic logic unit']:
            self._draw_alu_diagram(ax)
        elif 'adder' in component_type.lower():
            self._draw_adder_diagram(ax, parsed_spec.get("bit_width", 4))
        elif 'fsm' in component_type.lower() or 'state' in component_type.lower():
            self._draw_fsm_diagram(ax)
        elif 'uart' in component_type.lower():
            self._draw_uart_diagram(ax)
        else:
            self._draw_generic_diagram(ax, architecture)
        
        # Save to base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        plt.close()
        
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        return f"data:image/png;base64,{image_base64}"
    
    def _draw_alu_diagram(self, ax):
        """Draw ALU block diagram"""
        # Title
        ax.text(5, 9.5, 'ALU Block Diagram', ha='center', fontsize=16, fontweight='bold')
        
        # Input A
        ax.add_patch(patches.FancyBboxPatch((0.5, 6), 1.5, 1, boxstyle="round,pad=0.1", 
                                           facecolor='lightblue', edgecolor='black', linewidth=2))
        ax.text(1.25, 6.5, 'Input A\n[n-1:0]', ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Input B
        ax.add_patch(patches.FancyBboxPatch((0.5, 4), 1.5, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightblue', edgecolor='black', linewidth=2))
        ax.text(1.25, 4.5, 'Input B\n[n-1:0]', ha='center', va='center', fontsize=10, fontweight='bold')
        
        # OpCode
        ax.add_patch(patches.FancyBboxPatch((0.5, 2), 1.5, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightyellow', edgecolor='black', linewidth=2))
        ax.text(1.25, 2.5, 'OpCode\n[2:0]', ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Main ALU block
        ax.add_patch(patches.FancyBboxPatch((3.5, 2.5), 3, 5, boxstyle="round,pad=0.1",
                                           facecolor='lightcoral', edgecolor='black', linewidth=3))
        ax.text(5, 6.5, 'ALU Core', ha='center', fontsize=14, fontweight='bold')
        
        # Internal components
        ax.text(5, 5.5, '• Adder', ha='center', fontsize=9)
        ax.text(5, 5, '• Subtractor', ha='center', fontsize=9)
        ax.text(5, 4.5, '• AND Gate', ha='center', fontsize=9)
        ax.text(5, 4, '• OR Gate', ha='center', fontsize=9)
        ax.text(5, 3.5, '• XOR Gate', ha='center', fontsize=9)
        ax.text(5, 3, '• Shift Unit', ha='center', fontsize=9)
        
        # Output
        ax.add_patch(patches.FancyBboxPatch((8, 4.5), 1.5, 1.5, boxstyle="round,pad=0.1",
                                           facecolor='lightgreen', edgecolor='black', linewidth=2))
        ax.text(8.75, 5.25, 'Result\n[n-1:0]', ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Flags
        ax.add_patch(patches.FancyBboxPatch((8, 2.5), 1.5, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightyellow', edgecolor='black', linewidth=2))
        ax.text(8.75, 3, 'Flags\nZ,C,N,V', ha='center', va='center', fontsize=9)
        
        # Arrows
        ax.arrow(2, 6.5, 1.3, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(2, 4.5, 1.3, 0.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(2, 2.5, 1.3, 1.5, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(6.5, 5.25, 1.3, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
        ax.arrow(6.5, 3, 1.3, 0, head_width=0.2, head_length=0.2, fc='black', ec='black')
    
    def _draw_adder_diagram(self, ax, bit_width):
        """Draw adder block diagram"""
        ax.text(5, 9.5, f'{bit_width}-bit Ripple Carry Adder', ha='center', fontsize=16, fontweight='bold')
        
        num_blocks = min(bit_width, 4)  # Show max 4 blocks for clarity
        block_spacing = 8 / (num_blocks + 1)
        
        for i in range(num_blocks):
            x = 1 + i * block_spacing
            
            # Full adder block
            ax.add_patch(patches.Rectangle((x, 4), 1.5, 2, facecolor='lightblue', 
                                          edgecolor='black', linewidth=2))
            ax.text(x + 0.75, 5, f'FA{i}', ha='center', va='center', fontsize=12, fontweight='bold')
            
            # Inputs
            ax.text(x + 0.3, 6.5, f'A[{i}]', fontsize=8)
            ax.text(x + 1.2, 6.5, f'B[{i}]', fontsize=8)
            ax.arrow(x + 0.3, 6.3, 0, -0.2, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
            ax.arrow(x + 1.2, 6.3, 0, -0.2, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
            
            # Sum output
            ax.arrow(x + 0.75, 3.8, 0, -0.3, head_width=0.1, head_length=0.1, fc='green', ec='green')
            ax.text(x + 0.75, 3.2, f'S[{i}]', ha='center', fontsize=8, color='green')
            
            # Carry chain
            if i < num_blocks - 1:
                ax.arrow(x + 1.6, 5, block_spacing - 0.2, 0, head_width=0.15, head_length=0.15, 
                        fc='red', ec='red', linewidth=2)
                ax.text(x + block_spacing/2 + 1.5, 5.3, f'C{i}', ha='center', fontsize=8, color='red')
    
    def _draw_fsm_diagram(self, ax):
        """Draw FSM state diagram"""
        ax.text(5, 9.5, 'Finite State Machine', ha='center', fontsize=16, fontweight='bold')
        
        # States
        states = [
            {"name": "IDLE", "pos": (2, 6), "color": "lightgreen"},
            {"name": "ACTIVE", "pos": (5, 7), "color": "lightblue"},
            {"name": "PROCESS", "pos": (8, 6), "color": "lightyellow"},
            {"name": "DONE", "pos": (5, 4), "color": "lightcoral"}
        ]
        
        for state in states:
            circle = patches.Circle(state["pos"], 0.7, facecolor=state["color"], 
                                   edgecolor='black', linewidth=2)
            ax.add_patch(circle)
            ax.text(state["pos"][0], state["pos"][1], state["name"], 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Transitions
        ax.annotate('', xy=(4.3, 6.8), xytext=(2.7, 6.2),
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        ax.text(3.5, 6.8, 'start', fontsize=8, color='blue')
        
        ax.annotate('', xy=(7.3, 6.2), xytext=(5.7, 6.8),
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        ax.text(6.5, 6.8, 'enable', fontsize=8, color='blue')
        
        ax.annotate('', xy=(5.5, 4.7), xytext=(7.5, 5.5),
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        ax.text(7, 5, 'done', fontsize=8, color='blue')
        
        ax.annotate('', xy=(2.5, 5.5), xytext=(4.5, 4.7),
                   arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        ax.text(3, 5, 'reset', fontsize=8, color='blue')
    
    def _draw_uart_diagram(self, ax):
        """Draw UART block diagram"""
        ax.text(5, 9.5, 'UART Transmitter/Receiver', ha='center', fontsize=16, fontweight='bold')
        
        # TX path
        ax.add_patch(patches.FancyBboxPatch((1, 6), 1.5, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightblue', edgecolor='black', linewidth=2))
        ax.text(1.75, 6.5, 'TX FIFO', ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax.add_patch(patches.FancyBboxPatch((3.5, 6), 2, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightcoral', edgecolor='black', linewidth=2))
        ax.text(4.5, 6.5, 'Shift Register', ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax.add_patch(patches.FancyBboxPatch((6.5, 6), 1.5, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightgreen', edgecolor='black', linewidth=2))
        ax.text(7.25, 6.5, 'TX Pin', ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Arrows
        ax.arrow(2.5, 6.5, 0.8, 0, head_width=0.2, head_length=0.2, fc='black')
        ax.arrow(5.5, 6.5, 0.8, 0, head_width=0.2, head_length=0.2, fc='black')
        
        # Baud rate generator
        ax.add_patch(patches.FancyBboxPatch((3.5, 4), 2, 1, boxstyle="round,pad=0.1",
                                           facecolor='lightyellow', edgecolor='black', linewidth=2))
        ax.text(4.5, 4.5, 'Baud Rate\nGenerator', ha='center', va='center', fontsize=9, fontweight='bold')
        
        ax.arrow(4.5, 5, 0, 0.8, head_width=0.2, head_length=0.2, fc='red', linestyle='dashed')
    
    def _draw_generic_diagram(self, ax, architecture: Dict):
        """Draw generic component diagram"""
        ax.text(5, 9.5, 'Component Block Diagram', ha='center', fontsize=16, fontweight='bold')
        
        components = architecture.get('components', ['input', 'logic', 'output'])
        y_spacing = 6 / (len(components) + 1)
        
        for i, comp in enumerate(components[:5]):  # Max 5 components
            y = 7 - i * y_spacing
            ax.add_patch(patches.FancyBboxPatch((3, y - 0.4), 4, 0.8, boxstyle="round,pad=0.1",
                                               facecolor='lightblue', edgecolor='black', linewidth=2))
            ax.text(5, y, comp.upper(), ha='center', va='center', fontsize=11, fontweight='bold')
            
            if i < len(components) - 1:
                ax.arrow(5, y - 0.5, 0, -y_spacing + 0.6, head_width=0.3, head_length=0.2, 
                        fc='black', ec='black')

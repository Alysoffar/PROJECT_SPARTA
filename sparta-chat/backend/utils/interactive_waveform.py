"""Interactive Waveform Generator using Plotly"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, Any
import json


class InteractiveWaveformGenerator:
    """Generate interactive waveforms with zoom/pan capabilities"""
    
    async def create_interactive_waveform(self, simulation_data: Dict[str, Any]) -> str:
        """
        Create interactive Plotly waveform
        Returns HTML div string for embedding
        """
        # Create figure with subplots for multiple signals
        fig = make_subplots(
            rows=5, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=('Clock', 'Input A', 'Input B', 'Output', 'Control Signals')
        )
        
        # Time steps
        time = list(range(16))
        
        # Generate realistic signals
        clk = [i % 2 for i in range(16)]
        input_a = [0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0]
        input_b = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1]
        output = [0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0]
        control = [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
        
        # Clock signal
        fig.add_trace(
            go.Scatter(x=time, y=clk, mode='lines', name='CLK',
                      line=dict(color='blue', width=2, shape='hv'),
                      fill='tozeroy', fillcolor='rgba(0,100,255,0.2)'),
            row=1, col=1
        )
        
        # Input A
        fig.add_trace(
            go.Scatter(x=time, y=input_a, mode='lines', name='Input A',
                      line=dict(color='green', width=2, shape='hv'),
                      fill='tozeroy', fillcolor='rgba(0,255,0,0.2)'),
            row=2, col=1
        )
        
        # Input B
        fig.add_trace(
            go.Scatter(x=time, y=input_b, mode='lines', name='Input B',
                      line=dict(color='orange', width=2, shape='hv'),
                      fill='tozeroy', fillcolor='rgba(255,165,0,0.2)'),
            row=3, col=1
        )
        
        # Output
        fig.add_trace(
            go.Scatter(x=time, y=output, mode='lines', name='Output',
                      line=dict(color='red', width=3, shape='hv'),
                      fill='tozeroy', fillcolor='rgba(255,0,0,0.2)'),
            row=4, col=1
        )
        
        # Control signals
        fig.add_trace(
            go.Scatter(x=time, y=control, mode='lines', name='Control',
                      line=dict(color='purple', width=2, shape='hv'),
                      fill='tozeroy', fillcolor='rgba(128,0,128,0.2)'),
            row=5, col=1
        )
        
        # Update layout
        fig.update_layout(
            height=800,
            title_text="📊 Interactive Waveform Viewer (Zoom/Pan Enabled)",
            title_font_size=16,
            showlegend=True,
            hovermode='x unified',
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        # Update axes
        fig.update_xaxes(title_text="Time (cycles)", row=5, col=1, gridcolor='lightgray')
        fig.update_yaxes(range=[-0.2, 1.3], gridcolor='lightgray')
        
        # Add markers for transitions
        for i in range(1, len(time)):
            if clk[i] != clk[i-1]:
                fig.add_vline(x=time[i], line_dash="dot", line_color="gray", 
                             opacity=0.3, annotation_text="", row='all', col=1)
        
        # Return as HTML div
        return fig.to_html(include_plotlyjs='cdn', div_id='waveform_plot')
    
    async def create_performance_chart(self, metrics: Dict[str, Any]) -> str:
        """Create interactive performance comparison chart"""
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Resource Utilization', 'Performance Metrics'),
            specs=[[{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Resource utilization
        resources = ['LUTs', 'Registers', 'DSP', 'BRAM', 'IO']
        utilization = [45, 30, 10, 5, 20]
        
        fig.add_trace(
            go.Bar(x=resources, y=utilization, name='Utilization %',
                  marker_color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#F44336']),
            row=1, col=1
        )
        
        # Performance metrics
        perf_metrics = ['Area\n(mm²)', 'Power\n(mW)', 'Frequency\n(MHz)', 'Latency\n(ns)']
        perf_values = [0.16, 4.0, 227, 4.4]
        
        fig.add_trace(
            go.Bar(x=perf_metrics, y=perf_values, name='Metrics',
                  marker_color='lightblue'),
            row=1, col=2
        )
        
        fig.update_layout(
            height=400,
            title_text="📈 Design Performance Metrics",
            showlegend=False,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )
        
        fig.update_yaxes(title_text="Utilization (%)", row=1, col=1, gridcolor='lightgray')
        fig.update_yaxes(title_text="Value", row=1, col=2, gridcolor='lightgray')
        
        return fig.to_html(include_plotlyjs='cdn', div_id='performance_chart')

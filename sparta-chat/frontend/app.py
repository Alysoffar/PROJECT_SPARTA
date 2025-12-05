"""
SPARTA Hardware Design Assistant - Mechanical Engineering Interface
Professional CAD-style UI without emojis
"""
import streamlit as st
import requests
import uuid
from datetime import datetime
import os
import re
from pathlib import Path

# Backend API URL
BACKEND_URL = "http://localhost:9000"

# Page config - Engineering theme
st.set_page_config(
    page_title="SPARTA | Hardware Design Workstation",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    css = """
    <style>
    /* Import technical fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto+Mono:wght@300;400;500;700&display=swap');
    
    /* Global theme */
    :root {
        --steel-gray: #3A3F44;
        --matte-black: #1A1C1E;
        --engineering-blue: #3C6EAA;
        --brass-gold: #C8A951;
        --border-color: #4A4F54;
    }
    
    /* Main app background with blueprint grid */
    .stApp {
        background-color: var(--matte-black);
        background-image: 
            linear-gradient(rgba(60, 110, 170, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(60, 110, 170, 0.03) 1px, transparent 1px);
        background-size: 20px 20px;
        font-family: 'Roboto Mono', monospace;
        color: #E0E0E0;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: var(--brass-gold);
        text-transform: uppercase;
        letter-spacing: 2px;
        border-bottom: 2px solid var(--engineering-blue);
        padding-bottom: 8px;
        margin-top: 20px;
    }
    
    h1 {
        font-size: 28px;
        font-weight: 900;
    }
    
    h2 {
        font-size: 20px;
        font-weight: 700;
    }
    
    h3 {
        font-size: 16px;
        font-weight: 400;
    }
    
    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: var(--steel-gray);
        border-right: 3px solid var(--engineering-blue);
        box-shadow: inset -2px 0 10px rgba(0,0,0,0.5);
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: var(--steel-gray);
        border: 1px solid var(--border-color);
        border-radius: 2px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        margin: 10px 0;
        padding: 15px;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* User messages - right aligned */
    [data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"][aria-label="user"]) {
        background-color: rgba(60, 110, 170, 0.2);
        border-left: 3px solid var(--engineering-blue);
        margin-left: 20%;
    }
    
    /* Assistant messages - left aligned */
    [data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"][aria-label="assistant"]) {
        background-color: rgba(58, 63, 68, 0.8);
        border-left: 3px solid var(--brass-gold);
        margin-right: 20%;
    }
    
    /* Technical separator lines */
    hr {
        border: none;
        border-top: 1px solid var(--engineering-blue);
        margin: 20px 0;
        opacity: 0.5;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: var(--steel-gray);
        color: var(--brass-gold);
        border: 2px solid var(--engineering-blue);
        border-radius: 0;
        font-family: 'Orbitron', sans-serif;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        padding: 10px 20px;
        transition: all 0.3s;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    
    .stButton > button:hover {
        background-color: var(--engineering-blue);
        color: white;
        border-color: var(--brass-gold);
        box-shadow: 0 0 15px rgba(60, 110, 170, 0.5);
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: var(--matte-black);
        color: #E0E0E0;
        border: 1px solid var(--border-color);
        border-radius: 0;
        font-family: 'Roboto Mono', monospace;
        padding: 10px;
    }
    
    /* Chat input */
    .stChatInput > div {
        background-color: var(--steel-gray);
        border: 2px solid var(--engineering-blue);
        border-radius: 0;
    }
    
    .stChatInput input {
        background-color: var(--matte-black);
        color: #E0E0E0;
        font-family: 'Roboto Mono', monospace;
        border: none;
    }
    
    /* Images in chat */
    .chat-image {
        max-width: 100%;
        height: auto;
        border: 2px solid var(--engineering-blue);
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        margin: 15px 0;
        display: block;
    }
    
    .image-caption {
        font-size: 11px;
        color: var(--brass-gold);
        font-family: 'Roboto Mono', monospace;
        margin-top: 5px;
        text-align: center;
        letter-spacing: 1px;
    }
    
    /* Technical panels */
    .technical-panel {
        background-color: var(--steel-gray);
        border: 2px solid var(--engineering-blue);
        padding: 15px;
        margin: 10px 0;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
    }
    
    /* Metrics */
    .stMetric {
        background-color: var(--steel-gray);
        border: 1px solid var(--border-color);
        padding: 10px;
        border-radius: 0;
    }
    
    .stMetric label {
        color: var(--brass-gold);
        font-family: 'Orbitron', sans-serif;
        font-size: 12px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #E0E0E0;
        font-family: 'Roboto Mono', monospace;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: var(--steel-gray);
        border: 1px solid var(--border-color);
        font-family: 'Orbitron', sans-serif;
        color: var(--brass-gold);
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: var(--matte-black);
        border: 1px solid var(--engineering-blue);
        border-radius: 0;
    }
    
    /* Remove emoji styling */
    .stChatMessage [data-testid="chatAvatarIcon-user"],
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        display: none;
    }
    
    /* Status indicators */
    .status-success {
        color: #4CAF50;
        font-family: 'Roboto Mono', monospace;
        font-weight: 700;
    }
    
    .status-error {
        color: #F44336;
        font-family: 'Roboto Mono', monospace;
        font-weight: 700;
    }
    
    .status-warning {
        color: #FF9800;
        font-family: 'Roboto Mono', monospace;
        font-weight: 700;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background-color: var(--matte-black);
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: var(--engineering-blue);
        border: 1px solid var(--border-color);
    }
    
    /* Technical captions */
    .stCaption {
        color: #888;
        font-family: 'Roboto Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.5px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header with technical styling
st.markdown("""
<div style='text-align: center; padding: 20px 0; border-bottom: 3px solid #3C6EAA;'>
    <h1 style='margin: 0; font-size: 32px;'>SPARTA HARDWARE DESIGN WORKSTATION</h1>
    <p style='color: #C8A951; font-family: "Roboto Mono", monospace; margin: 5px 0 0 0; letter-spacing: 2px;'>
        MULTI-AGENT RTL GENERATION SYSTEM | VERSION 2.0
    </p>
</div>
""", unsafe_allow_html=True)

# Layout: Two columns
col_chat, col_tools = st.columns([2, 1])

# Left Panel - Chat Interface
with col_chat:
    st.markdown("### DESIGN CONSOLE")
    
    # Display chat messages
    for idx, msg in enumerate(st.session_state.messages):
        role = msg["role"]
        content = msg["content"]
        
        with st.chat_message(role):
            # Parse and display content sections
            if role == "assistant":
                st.markdown("**RESPONSE**")
                st.markdown("---")
            
            # Check for images in content
            if "![diagram]" in content or "![image]" in content:
                # Extract image path
                img_match = re.search(r'!\[.*?\]\((.*?)\)', content)
                if img_match:
                    img_path = img_match.group(1)
                    
                    # Remove image markdown from text
                    display_content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
                    st.markdown(display_content)
                    
                    # Display image
                    full_img_url = f"{BACKEND_URL}/{img_path}"
                    try:
                        st.markdown(f'<img src="{full_img_url}" class="chat-image">', unsafe_allow_html=True)
                        st.markdown(f'<p class="image-caption">GENERATED DIAGRAM | {os.path.basename(img_path)}</p>', unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown(f'<p class="status-error">IMAGE LOAD FAILED: {img_path}</p>', unsafe_allow_html=True)
                        st.markdown(f'<p class="status-warning">Attempting reload from: {full_img_url}</p>', unsafe_allow_html=True)
            else:
                st.markdown(content)
            
            # Show visualization if present
            if "visualization" in msg and msg["visualization"]:
                st.markdown("---")
                st.markdown("**WAVEFORM ANALYSIS**")
                st.image(msg["visualization"], use_column_width=True)
            
            # Show download links if present
            if "download_links" in msg and msg["download_links"]:
                st.markdown("---")
                st.markdown("**AVAILABLE DOWNLOADS**")
                links = msg["download_links"]
                
                link_cols = st.columns(len(links))
                for idx, (name, url) in enumerate(links.items()):
                    with link_cols[idx]:
                        display_name = name.replace("_", " ").upper()
                        st.markdown(f"[{display_name}]({BACKEND_URL}{url})")
            
            # Show internal notes if present
            if "internal_notes" in msg and msg["internal_notes"]:
                with st.expander("SYSTEM DIAGNOSTICS"):
                    st.code(msg["internal_notes"], language="text")

# Chat input
if prompt := st.chat_input("ENTER DESIGN SPECIFICATION..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message immediately
    with col_chat:
        with st.chat_message("user"):
            st.markdown(prompt)
    
    # Call backend
    with col_chat:
        with st.chat_message("assistant"):
            with st.spinner("PROCESSING REQUEST..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={
                            "session_id": st.session_state.session_id,
                            "message": prompt
                        },
                        timeout=120
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Display response
                        st.markdown("**RESPONSE**")
                        st.markdown("---")
                        
                        response_text = data["response"]
                        
                        # Handle images in response
                        if "![diagram]" in response_text or "![image]" in response_text:
                            img_match = re.search(r'!\[.*?\]\((.*?)\)', response_text)
                            if img_match:
                                img_path = img_match.group(1)
                                
                                # Remove image markdown from text
                                display_content = re.sub(r'!\[.*?\]\(.*?\)', '', response_text)
                                st.markdown(display_content)
                                
                                # Display image
                                full_img_url = f"{BACKEND_URL}/{img_path}"
                                st.markdown(f'<img src="{full_img_url}" class="chat-image">', unsafe_allow_html=True)
                                st.markdown(f'<p class="image-caption">GENERATED DIAGRAM | {os.path.basename(img_path)}</p>', unsafe_allow_html=True)
                        else:
                            st.markdown(response_text)
                        
                        # Show visualization if available
                        if data.get("visualization"):
                            st.markdown("---")
                            st.markdown("**WAVEFORM ANALYSIS**")
                            st.image(data["visualization"], use_column_width=True)
                        
                        # Show download links
                        if data.get("download_links"):
                            st.markdown("---")
                            st.markdown("**AVAILABLE DOWNLOADS**")
                            links = data["download_links"]
                            
                            link_cols = st.columns(len(links))
                            for idx, (name, url) in enumerate(links.items()):
                                with link_cols[idx]:
                                    display_name = name.replace("_", " ").upper()
                                    st.markdown(f"[{display_name}]({BACKEND_URL}{url})")
                        
                        # Show internal notes
                        if data.get("internal_notes"):
                            with st.expander("SYSTEM DIAGNOSTICS"):
                                st.code(data["internal_notes"], language="text")
                        
                        # Save to session
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": data["response"],
                            "visualization": data.get("visualization"),
                            "download_links": data.get("download_links"),
                            "internal_notes": data.get("internal_notes"),
                            "metadata": data.get("metadata")
                        })
                        
                        st.rerun()
                    else:
                        st.markdown(f'<p class="status-error">BACKEND ERROR: STATUS {response.status_code}</p>', unsafe_allow_html=True)
                
                except requests.exceptions.Timeout:
                    st.markdown('<p class="status-error">REQUEST TIMEOUT: DESIGN COMPLEXITY EXCEEDED TIME LIMIT</p>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<p class="status-error">SYSTEM ERROR: {str(e)}</p>', unsafe_allow_html=True)

# Right Panel - Tools & Metrics
with col_tools:
    st.markdown("### SYSTEM STATUS")
    
    # Session info
    with st.container():
        st.markdown('<div class="technical-panel">', unsafe_allow_html=True)
        st.markdown("**SESSION INFORMATION**")
        st.text(f"ID: {st.session_state.session_id[:16]}...")
        st.text(f"MESSAGES: {len(st.session_state.messages)}")
        st.text(f"TIMESTAMP: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("NEW SESSION"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    
    # Design metrics from last response
    if st.session_state.messages:
        last_msg = st.session_state.messages[-1]
        if last_msg["role"] == "assistant" and "metadata" in last_msg:
            metadata = last_msg["metadata"]
            
            st.markdown("**DESIGN METRICS**")
            
            if "metrics" in metadata and metadata["metrics"]:
                metrics = metadata["metrics"]
                st.metric("AREA", f"{metrics.get('area_mm2', 'N/A')} mm²")
                st.metric("POWER", f"{metrics.get('power_mw', 'N/A')} mW")
                st.metric("LATENCY", f"{metrics.get('latency_ns', 'N/A')} ns")
            
            if "simulation_status" in metadata:
                status = metadata["simulation_status"]
                status_class = "status-success" if status == "completed" else "status-warning"
                st.markdown(f'<p class="{status_class}">SIMULATION: {status.upper()}</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick examples
    st.markdown("**DESIGN TEMPLATES**")
    examples = [
        "4-BIT RIPPLE CARRY ADDER",
        "8-BIT ALU WITH OPERATIONS",
        "TRAFFIC LIGHT FSM CONTROLLER",
        "UART TRANSMITTER MODULE"
    ]
    
    for example in examples:
        if st.button(example, key=example):
            st.session_state.messages.append({"role": "user", "content": example.lower()})
            st.rerun()
    
    st.markdown("---")
    
    # Search
    st.markdown("**DESIGN ARCHIVE**")
    search_query = st.text_input("SEARCH PREVIOUS DESIGNS", key="search")
    if search_query:
        try:
            response = requests.get(
                f"{BACKEND_URL}/search",
                params={"query": search_query, "limit": 5}
            )
            if response.status_code == 200:
                results = response.json()["results"]
                if results:
                    for result in results:
                        spec = result.get("spec", {})
                        st.text(f"- {spec.get('component', 'UNKNOWN').upper()}")
                else:
                    st.text("NO RESULTS FOUND")
        except:
            st.text("SEARCH UNAVAILABLE")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #888; font-family: "Roboto Mono", monospace; font-size: 11px;'>
    SPARTA V2.0 | MULTI-AGENT HARDWARE DESIGN SYSTEM | MECHANICAL ENGINEERING INTERFACE
</div>
""", unsafe_allow_html=True)

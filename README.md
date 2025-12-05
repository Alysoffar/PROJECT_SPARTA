# SPARTA - Hardware Design and Optimization Platform

SPARTA is an AI-native platform that accelerates hardware design through intelligent hardware specification synthesis, RTL generation, and interactive circuit visualization with a conversational interface.

## Overview

SPARTA combines automated hardware description generation with an intuitive chat-based interface to help engineers and developers quickly design, simulate, and optimize digital circuits. The platform generates production-ready RTL code, produces circuit schematics and breadboard diagrams, and provides comprehensive design documentation.

## Key Features

- Conversational Chat Interface: Natural language hardware design specifications
- RTL Code Generation: Automatic Verilog/SystemVerilog code synthesis
- Circuit Visualization: Breadboard diagrams with component-specific wiring and bill of materials
- Hardware Support: Adders, ALUs, counters, registers, UARTs, multiplexers, flip-flops
- Design Export: Download RTL, testbenches, reports, PCB layouts, and Gerber files
- Multi-Agent Architecture: Specialized agents for planning, synthesis, RTL generation, and simulation
- Session Memory: Design context persistence across chat interactions

## Architecture

```
Frontend (Streamlit)
        |
        v
API Gateway (FastAPI - Port 9000)
        |
        +-------> Chat Endpoint
        |
        +-------> Image Generation Endpoint
        |
        v
Backend Agents
    - Planning Agent (task breakdown)
    - Synthesis Agent (architecture generation)
    - RTL Agent (Verilog/SystemVerilog)
    - Image Agent (breadboard diagrams)
    - Emulation Agent (simulation/verification)
    |
    v
SQLite Database (session memory, chat history)
```

## Project Structure

```
TestProject/
├── docs/                           # Documentation
├── sparta-chat/
│   ├── backend/                    # FastAPI backend server
│   │   ├── agents/                 # Multi-agent system
│   │   │   ├── image_agent.py      # Breadboard diagram generation
│   │   │   ├── planning_agent.py   # Task decomposition
│   │   │   ├── synthesis_agent.py  # Architecture synthesis
│   │   │   ├── rtl_agent.py        # RTL/Verilog generation
│   │   │   ├── nlp_agent.py        # Natural language parsing
│   │   │   └── emulation_agent.py  # Simulation and verification
│   │   ├── downloads.py            # Artifact export endpoints
│   │   ├── main.py                 # FastAPI orchestrator
│   │   ├── database.py             # SQLite interface
│   │   └── requirements.txt
│   ├── frontend/
│   │   └── app.py                  # Streamlit chat UI
│   └── static/                     # Generated diagrams and images
└── [service modules and other infrastructure]
```

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
git clone <repository-url>
cd TestProject
docker-compose up -d

# Access the application:
# Frontend: http://localhost:8501
# Backend API: http://localhost:9000
# API Docs: http://localhost:9000/docs
```

### Option 2: Local Python Installation

```bash
cd TestProject/sparta-chat

# Install dependencies
pip install -r requirements.txt

# Start the backend (Terminal 1)
cd backend
python main.py

# Start the frontend (Terminal 2)
cd ../frontend
streamlit run app.py
```

For detailed setup instructions, see [docs/QUICK_START.md](docs/QUICK_START.md)

## Usage Examples

### Generate an Adder Circuit

```
User: "Create a 4-bit ripple-carry adder with inputs A and B"

System Response:
- Generates architecture specification
- Creates Verilog RTL code
- Produces breadboard diagram with:
  * Arduino/MCU connections
  * 74LS83 4-bit adder IC with labeled pins
  * Input/output signal routing
  * Bill of materials
```

### Request a Custom ALU

```
User: "Design an 8-bit ALU with A, B inputs and 3-bit function select"

System Response:
- Synthesizes ALU architecture
- Generates SystemVerilog implementation
- Creates circuit diagram with 74LS181 ALU IC pinout
- Produces PCB and Gerber files
```

## Supported Hardware Components

Adders, ALUs, counters, registers, UARTs, multiplexers, flip-flops with accurate pinouts, wiring, and bill of materials.

## Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Get running in 5 minutes
- [Architecture Guide](docs/architecture.md) - System design details
- [API Reference](docs/api-reference.md) - Complete endpoint documentation
- [Image Generation Guide](docs/IMAGE_GENERATION_GUIDE.md) - Diagram generation
- [Deployment Guide](docs/deployment.md) - Production setup
- [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and solutions

## System Requirements

- Python 3.9+
- 4GB RAM minimum
- 2GB disk space
- Modern web browser

## Technology Stack

- Backend: FastAPI, Python
- Frontend: Streamlit
- Diagrams: Matplotlib
- Database: SQLite
- Container: Docker & Docker Compose

## License

MIT License - see LICENSE file

## Contributing

Contributions welcome. See docs/development.md for guidelines.

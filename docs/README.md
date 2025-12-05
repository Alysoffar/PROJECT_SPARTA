# SPARTA Documentation

Complete documentation for the SPARTA hardware design platform.

## Getting Started

Start here if you're new to SPARTA:

1. [Quick Start](QUICK_START.md) - Get the system running in 5 minutes
2. [Quick Reference](QUICK_REFERENCE.md) - Common commands and URLs
3. [Architecture](architecture.md) - Understand the system design

## Core Documentation

### System Design and Architecture

- [Architecture Guide](architecture.md) - Complete system architecture, components, and data flow
- [API Reference](api-reference.md) - All API endpoints with request/response examples

### Setup and Deployment

- [Quick Start](QUICK_START.md) - Initial setup guide (Docker and local installation)
- [Deployment Guide](deployment.md) - Production deployment, scaling, monitoring
- [Running Without Docker](RUNNING_WITHOUT_DOCKER.md) - Local Python installation steps

### Features and Guides

- [Image Generation Guide](IMAGE_GENERATION_GUIDE.md) - Breadboard diagram generation, component details, customization
- [Mechanical Theme Update](MECHANICAL_THEME_UPDATE.md) - Frontend styling and UI customization

### Development

- [Development Guide](development.md) - Coding standards, development workflow, testing
- [Quick Reference](QUICK_REFERENCE.md) - Common URLs, commands, example requests

### Troubleshooting

- [Troubleshooting Guide](TROUBLESHOOTING.md) - Common issues, diagnostics, solutions
- [Quickstart](quickstart.md) - Quick setup reference

## Documentation Organization

```
docs/
├── README.md                          # This file
├── QUICK_START.md                     # Initial setup (5 minutes)
├── QUICK_REFERENCE.md                 # Common commands and URLs
├── TROUBLESHOOTING.md                 # Problem resolution
├── RUNNING_WITHOUT_DOCKER.md          # Local Python setup
├── architecture.md                    # System design details
├── api-reference.md                   # API endpoint documentation
├── deployment.md                      # Production deployment
├── development.md                     # Development standards and workflow
├── IMAGE_GENERATION_GUIDE.md          # Circuit diagram generation
├── MECHANICAL_THEME_UPDATE.md         # UI/styling details
└── quickstart.md                      # Quick reference guide
```

## Key Topics

### Installation

- Docker: Follow [Quick Start](QUICK_START.md)
- Local Python: See [Running Without Docker](RUNNING_WITHOUT_DOCKER.md)
- Configuration: Check [Deployment Guide](deployment.md) for environment variables

### Usage

- Chat Interface: Use natural language to describe your hardware design
- Image Generation: Automatic breadboard diagrams with component-specific wiring
- Design Export: Download RTL code, testbenches, reports, PCB files
- Examples: See [Image Generation Guide](IMAGE_GENERATION_GUIDE.md)

### API

- Chat Endpoint: `POST /chat`
- Image Generation: `POST /generate_image`
- Downloads: `GET /download/{type}/{design_id}`
- Complete reference: [API Reference](api-reference.md)

### Troubleshooting

Common issues and solutions in [Troubleshooting Guide](TROUBLESHOOTING.md)

- Backend won't start
- Frontend can't connect
- Images not generating
- Port conflicts
- Database issues

## Architecture Overview

SPARTA uses a modular multi-agent architecture:

```
Chat Interface (Streamlit)
           |
    FastAPI Backend (Port 9000)
           |
    +------+------+------+------+
    |      |      |      |      |
  Planning NLP  Synthesis RTL  Image
   Agent  Agent  Agent    Agent Agent
    |      |      |      |      |
    +------+------+------+------+
           |
       SQLite Database
```

## Supported Components

The system generates realistic breadboard diagrams for:

- Adders: Half-adder, Full-adder, Ripple-carry (74LS83), Carry-lookahead (74LS182)
- ALU: 8-bit ALU (74LS181) with function select
- Counter: Async (74LS390), Sync (74LS161)
- Register: Shift (74LS595), Parallel load (74LS173)
- MUX/DEMUX: Multiplexer (74LS153), Demultiplexer (74LS139)
- UART: Serial communication (MAX232)
- Flip-Flops: D (74LS74), JK (74LS109)

Each diagram includes:
- Accurate pin assignments
- Component-specific wiring
- Bill of materials
- Color-coded signal routing
- Power and ground connections

## System Requirements

- Python 3.9+
- 4GB RAM
- 2GB disk space
- Modern web browser
- Docker (optional, for containerized deployment)

## Performance

- Chat response: 2-5 seconds
- Image generation: 1-2 seconds
- RTL generation: 3-8 seconds
- File export: 500ms-2 seconds

## Technology Stack

- Backend: FastAPI, Python 3.9+
- Frontend: Streamlit
- Diagrams: Matplotlib
- Database: SQLite
- Container: Docker & Docker Compose

## Code Location

Key files in the repository:

```
sparta-chat/
├── backend/
│   ├── main.py              # FastAPI server and chat endpoint
│   ├── agents/
│   │   ├── image_agent.py   # Breadboard diagram generation
│   │   ├── rtl_agent.py     # Verilog/SystemVerilog code
│   │   └── [other agents]
│   ├── downloads.py         # Artifact export endpoints
│   └── database.py          # Session and history storage
└── frontend/
    └── app.py               # Streamlit UI
```

## Documentation Navigation

**Need to...**

- Set up the system? Start with [Quick Start](QUICK_START.md)
- Find an API endpoint? See [API Reference](api-reference.md)
- Deploy to production? Read [Deployment Guide](deployment.md)
- Understand the architecture? Check [Architecture Guide](architecture.md)
- Fix an issue? Look in [Troubleshooting Guide](TROUBLESHOOTING.md)
- Learn about image generation? See [Image Generation Guide](IMAGE_GENERATION_GUIDE.md)
- Start development? Read [Development Guide](development.md)

## Questions or Issues?

1. Check [Troubleshooting Guide](TROUBLESHOOTING.md) for common issues
2. Review relevant guide above
3. Report issues on GitHub with detailed error messages and steps to reproduce

## Contributing

See [Development Guide](development.md) for contributing guidelines.

---

Last updated: 2024
For the latest information, see individual documentation files.

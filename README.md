# SPARTA — Superhuman PRAgmatic Technology Accelerator

**An AI-native hardware design and optimization platform with integrated circuit emulation, RTL generation, and multi-objective optimization.**

## 🎯 Project Vision

SPARTA is a comprehensive platform that accelerates hardware design by combining:
- AI-driven hardware specification synthesis
- Multi-paradigm compiler infrastructure
- RTL generation and optimization
- Cycle-accurate circuit emulation
- Multi-objective design space exploration

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)             │
│              Chat UI, Design Canvas, Visualization           │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                 API Gateway (FastAPI)                        │
│          Authentication, Rate Limiting, Routing              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│              AI Orchestrator (Python)                        │
│     Task Decomposition, Agent Coordination, Workflow Mgmt    │
└─────┬───────┬───────┬───────┬───────┬───────┬──────────────┘
      │       │       │       │       │       │
      ▼       ▼       ▼       ▼       ▼       ▼
   ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
   │NLP │ │RTL │ │Opt │ │Emu │ │Syn │ │Viz │  Specialized Agents
   │Agt │ │Gen │ │Agt │ │Svc │ │Agt │ │Agt │
   └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
```

## 📁 Project Structure

```
TestProject/
├── frontend/              # React TypeScript UI
├── gateway/               # FastAPI gateway service
├── orchestrator/          # AI orchestrator service
├── agents/
│   ├── nlp-agent/        # Natural language processing
│   ├── synthesis-agent/  # Hardware specification synthesis
│   ├── optimization-agent/ # Multi-objective optimization
│   └── visualization-agent/ # Data visualization
├── services/
│   ├── emulator/         # Cycle-accurate emulation
│   ├── rtl-generator/    # RTL code generation
│   ├── compiler/         # Multi-paradigm compiler
│   └── model-synthesis/  # Hardware model synthesis
├── shared/
│   ├── schemas/          # Shared data schemas
│   ├── utils/            # Shared utilities
│   └── proto/            # Protocol buffers (if needed)
├── infrastructure/
│   ├── docker/           # Dockerfiles
│   ├── kubernetes/       # K8s manifests
│   └── terraform/        # IaC configs
├── tests/                # Integration tests
└── docs/                 # Documentation
```

## 🚀 Quick Start

### Prerequisites

**Required**:
- **Docker Desktop 4.0+** - [Download here](https://www.docker.com/products/docker-desktop)
  - ⚠️ **Not installed?** See **[INSTALL_DOCKER.md](INSTALL_DOCKER.md)** for setup help

**Optional** (for running tests):
- PowerShell (Windows) or Bash (Linux/Mac)
- Python 3.11+

### Windows - Quick Start

```powershell
# Start all services (auto-detects Docker Desktop)
.\scripts\start.ps1

# Access points:
#   Frontend:     http://localhost:3000
#   API Gateway:  http://localhost:8000
#   API Docs:     http://localhost:8000/docs

# View logs
docker compose logs -f

# Run integration tests
pip install -r tests\requirements.txt
pytest tests\test_integration.py -v
```

**📖 First time user?** See **[QUICK_START.md](QUICK_START.md)** for detailed setup instructions.

**⚠️ Having issues?** See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for solutions to common problems.

### Linux/Mac - Quick Start

```bash
# Start all services
docker compose up -d

# Check health
curl http://localhost:8000/health

# Run tests
pip install -r tests/requirements.txt
pytest tests/test_integration.py -v
```

### Individual Service Development

See service-specific READMEs:
- [Frontend](./frontend/README.md)
- [Gateway](./gateway/README.md)
- [Orchestrator](./orchestrator/README.md)
- [Emulator](./services/emulator/README.md)

## 🧪 Testing

```bash
# Run all tests
./scripts/test-all.sh

# Run specific service tests
cd services/emulator && pytest
cd agents/nlp-agent && pytest
```

## 📚 Documentation

- [Architecture Guide](./docs/architecture.md)
- [API Reference](./docs/api-reference.md)
- [Development Guide](./docs/development.md)
- [Deployment Guide](./docs/deployment.md)

## 🛠️ Technology Stack

**Frontend:**
- React 18 + TypeScript
- TanStack Query (data fetching)
- Zustand (state management)
- TailwindCSS (styling)
- Recharts (visualization)

**Backend:**
- FastAPI (gateway & services)
- LangChain (AI orchestration)
- PostgreSQL (data persistence)
- Redis (caching)
- RabbitMQ (message queue)

**Infrastructure:**
- Docker & Docker Compose
- Kubernetes
- Terraform
- GitHub Actions (CI/CD)

## 📄 License

MIT License - see [LICENSE](./LICENSE) file

## 🤝 Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for development guidelines.

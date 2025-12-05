# SPARTA Quick Start Guide

## Prerequisites

### Required Software

1. **Docker Desktop** (v4.0+)
   - Download: https://www.docker.com/products/docker-desktop
   - Ensure Docker Desktop is running before starting SPARTA
   - Requires WSL2 on Windows 10/11

2. **Python** (3.11+)
   - Only needed if running tests
   - Download: https://www.python.org/downloads/

### System Requirements

- **RAM**: 8GB minimum, 16GB recommended
- **Disk**: 10GB free space
- **CPU**: 4 cores recommended
- **OS**: Windows 10/11, macOS, or Linux

## First-Time Setup

### Step 1: Verify Docker Installation

```powershell
# Check Docker is installed
docker --version
# Should show: Docker version 24.x.x or higher

# Check Docker Desktop is running
docker ps
# Should show container list (may be empty)
```

If Docker command not found:
1. Install Docker Desktop
2. Start Docker Desktop from Start Menu
3. Wait for "Docker Desktop is running" in system tray
4. Restart PowerShell

### Step 2: Start SPARTA

```powershell
# Navigate to project directory
cd d:\WORK\projects\TestProject

# Run the quick start script
.\scripts\start.ps1
```

**What happens**:
1. ✅ Script finds Docker Desktop
2. ✅ Starts Docker if not running
3. ✅ Builds all service images (~5 min first time)
4. ✅ Starts 14 services (3 infrastructure + 11 application)
5. ✅ Waits for services to become healthy
6. ✅ Shows status of each service

**Expected output**:
```
SPARTA Quick Start
==================

✓ Docker found: C:\Program Files\Docker\Docker\resources\bin\docker.exe
✓ Docker Desktop is running

Starting services with Docker Compose...
[+] Building 234.5s (89/89) FINISHED
[+] Running 14/14
 ✓ Container postgres    Started
 ✓ Container redis       Started
 ✓ Container rabbitmq    Started
 ✓ Container gateway     Started
 ✓ Container orchestrator Started
 ... (all services)

Waiting for services to become healthy...............

✓ All core services are healthy!

Services Status:
  ✓ Gateway
  ✓ Orchestrator
  ✓ NLP Agent
  ✓ Synthesis Agent
  ✓ Emulator
  ✓ RTL Generator

Access Points:
  Frontend:     http://localhost:3000
  API Gateway:  http://localhost:8000
  Orchestrator: http://localhost:8001
  Swagger Docs: http://localhost:8000/docs

✓ SPARTA is ready!
```

### Step 3: Verify Services

Open browser to:
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Running Tests

### Setup Test Environment

```powershell
# Install test dependencies
pip install -r tests\requirements.txt
```

### Run Integration Tests

```powershell
# Make sure services are running first!
pytest tests\test_integration.py -v
```

**Expected output**:
```
tests/test_integration.py::test_end_to_end_workflow 
Waiting for Gateway at http://localhost:8000/health...
✓ Gateway is ready
Waiting for Orchestrator at http://localhost:8001/health...
✓ Orchestrator is ready
PASSED

tests/test_integration.py::test_health_checks 
✓ Gateway: healthy
✓ Orchestrator: healthy
✓ NLP Agent: healthy
✓ Synthesis Agent: healthy
✓ Emulator: healthy
✓ RTL Generator: healthy
PASSED

=============== 2 passed in 15.2s ===============
```

## Common Commands

### View Logs

```powershell
# All services
docker compose logs -f

# Specific service
docker compose logs -f gateway

# Last 100 lines
docker compose logs --tail=100 gateway
```

### Check Service Status

```powershell
# List all containers
docker compose ps

# Resource usage
docker stats

# Network connections
docker compose ps --format table
```

### Restart Services

```powershell
# Restart single service
docker compose restart gateway

# Restart all
docker compose restart

# Stop all
docker compose down

# Start again
.\scripts\start.ps1
```

### Clean Restart

```powershell
# Stop and remove containers + volumes
docker compose down -v

# Fresh start
.\scripts\start.ps1
```

## Service Ports

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | React web UI |
| Gateway | 8000 | Main API entry point |
| Orchestrator | 8001 | Workflow coordination |
| NLP Agent | 8010 | Natural language processing |
| Synthesis Agent | 8011 | Logic synthesis |
| Verification Agent | 8012 | Formal verification |
| Planning Agent | 8013 | Task planning |
| Emulator | 8020 | Hardware emulation |
| RTL Generator | 8021 | RTL code generation |
| Constraints Solver | 8022 | Constraint solving |
| Optimizer | 8023 | Design optimization |
| Postgres | 5432 | Database |
| Redis | 6379 | Cache |
| RabbitMQ | 5672 | Message queue |
| RabbitMQ UI | 15672 | Management interface |

## Development Workflow

### Make Code Changes

1. Edit Python files in `gateway/`, `orchestrator/`, `agents/`, or `services/`
2. Restart affected service:
   ```powershell
   docker compose restart gateway
   ```
3. Check logs:
   ```powershell
   docker compose logs -f gateway
   ```

### Rebuild After Dependencies Change

```powershell
# Rebuild specific service
docker compose up -d --build gateway

# Rebuild everything
docker compose down
.\scripts\start.ps1
```

### Add New Python Package

1. Edit `<service>/requirements.txt`
2. Rebuild service:
   ```powershell
   docker compose build gateway
   docker compose up -d gateway
   ```

## Troubleshooting

### Services Don't Start

**Check Docker Desktop**:
- Is Docker Desktop running? (Check system tray)
- Enough resources allocated? (Settings → Resources)
  - Recommended: 4 CPUs, 8GB RAM

**Check Ports**:
```powershell
# See what's using port 8000
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
```

**Clean restart**:
```powershell
docker compose down -v
.\scripts\start.ps1
```

### Tests Fail

**Ensure services are running**:
```powershell
# Check health
curl http://localhost:8000/health

# If not running
.\scripts\start.ps1
```

**Wait for initialization**:
Services can take 1-2 minutes to fully start on first run.

### Slow Performance

**Allocate more resources**:
1. Docker Desktop → Settings → Resources
2. Increase CPUs to 4+
3. Increase Memory to 8GB+
4. Click "Apply & Restart"

**Use WSL2 backend** (Windows):
- Docker Desktop → Settings → General
- Enable "Use WSL2 based engine"

### See Full Troubleshooting Guide

For detailed solutions: `TROUBLESHOOTING.md`

## Next Steps

1. **Explore API**: http://localhost:8000/docs
2. **Read Architecture**: `docs/architecture.md`
3. **Review API Reference**: `docs/api-reference.md`
4. **Development Guide**: `docs/development.md`

## Getting Help

Run into issues? Check:
1. `TROUBLESHOOTING.md` - Common issues and solutions
2. `docker compose logs` - Service logs
3. `docs/` directory - Comprehensive documentation

## Stopping SPARTA

```powershell
# Stop all services (keeps data)
docker compose stop

# Stop and remove containers (keeps data)
docker compose down

# Remove everything including data
docker compose down -v
```

To restart: `.\scripts\start.ps1`

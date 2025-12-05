# Running SPARTA Without Docker (Development Mode)

## Prerequisites

- Python 3.11+
- PostgreSQL 14+ (running locally)
- Redis 6+ (running locally)
- RabbitMQ 3.11+ (running locally)

## Environment Setup

### 1. Install Python Dependencies

Each service has its own requirements.txt:

```powershell
# Gateway
cd gateway
pip install -r requirements.txt

# Orchestrator
cd ..\orchestrator
pip install -r requirements.txt

# Agents (repeat for each)
cd ..\agents\nlp-agent
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in each service directory:

**gateway/.env**:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sparta
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
```

**orchestrator/.env**:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/sparta
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### 3. Start Infrastructure Services

**Option A: Use Docker for infrastructure only**
```powershell
# Start just Postgres, Redis, RabbitMQ
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres --name sparta-postgres postgres:14
docker run -d -p 6379:6379 --name sparta-redis redis:7-alpine
docker run -d -p 5672:5672 -p 15672:15672 --name sparta-rabbitmq rabbitmq:3.11-management
```

**Option B: Install natively on Windows**
- PostgreSQL: https://www.postgresql.org/download/windows/
- Redis: https://github.com/microsoftarchive/redis/releases
- RabbitMQ: https://www.rabbitmq.com/install-windows.html

### 4. Run Services Manually

Open separate PowerShell windows for each:

**Terminal 1 - Gateway**:
```powershell
cd d:\WORK\projects\TestProject\gateway
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/sparta"
$env:REDIS_URL="redis://localhost:6379/0"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Orchestrator**:
```powershell
cd d:\WORK\projects\TestProject\orchestrator
$env:DATABASE_URL="postgresql://postgres:postgres@localhost:5432/sparta"
$env:RABBITMQ_URL="amqp://guest:guest@localhost:5672/"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 3 - NLP Agent**:
```powershell
cd d:\WORK\projects\TestProject\agents\nlp-agent
python -m uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```

**Terminal 4 - Frontend** (optional):
```powershell
cd d:\WORK\projects\TestProject\frontend
npm install
npm start
```

### 5. Run Integration Tests

Once services are running:

```powershell
cd d:\WORK\projects\TestProject
pytest tests\test_integration.py -v
```

## Limitations of Non-Docker Setup

⚠️ **This approach has several drawbacks**:

1. **Manual dependency management** - Must install Postgres, Redis, RabbitMQ separately
2. **Port conflicts** - May conflict with other services on your machine
3. **Environment inconsistency** - Different from production Docker setup
4. **More complex** - Requires managing multiple terminal windows
5. **Database persistence** - Need to manually manage database migrations

## Recommended: Install Docker Desktop

Docker Desktop provides:
- ✅ One-command startup: `.\scripts\start.ps1`
- ✅ Isolated environment
- ✅ Production-identical setup
- ✅ Easy cleanup: `docker compose down`
- ✅ No port conflicts
- ✅ Automated health checks

**Download**: https://www.docker.com/products/docker-desktop

After installing Docker Desktop, simply run:
```powershell
.\scripts\start.ps1
```

## Current Status

Your system status:
- ❌ Docker Desktop: Not installed
- ✅ Python: Installed (3.13.5)
- ✅ pytest: Installed
- ✅ httpx: Installed (0.28.1)

**Next step**: Install Docker Desktop for the best experience.

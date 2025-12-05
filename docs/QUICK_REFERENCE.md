# SPARTA Quick Reference

## 🚀 Quick Start

```powershell
# Start all services
.\scripts\start.ps1

# Or manually
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🌐 Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | User interface |
| API Gateway | http://localhost:8000 | Main API entry |
| Swagger Docs | http://localhost:8000/docs | API documentation |
| Orchestrator | http://localhost:8001 | Workflow management |
| NLP Agent | http://localhost:8010 | Text parsing |
| Synthesis Agent | http://localhost:8011 | Architecture synthesis |
| Optimization Agent | http://localhost:8012 | Design optimization |
| Visualization Agent | http://localhost:8013 | Data visualization |
| Emulator | http://localhost:8020 | Hardware emulation |
| RTL Generator | http://localhost:8021 | RTL code generation |
| Model Synthesis | http://localhost:8022 | Model transformation |
| Compiler | http://localhost:8023 | Code compilation |
| RabbitMQ UI | http://localhost:15672 | Message queue (sparta/sparta_dev_password) |

## 📝 Example Requests

### Create Workflow
```bash
curl -X POST http://localhost:8000/api/v1/workflows \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Create a 32-bit adder with low power consumption"
  }'
```

### Check Workflow Status
```bash
curl http://localhost:8000/api/v1/workflows/{workflow_id}
```

### Run Emulation
```bash
curl -X POST http://localhost:8020/emulate \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": [
      {"opcode": "ADD", "operands": ["r1", "r2", "r3"]},
      {"opcode": "NOP", "operands": []}
    ],
    "num_cycles": 10,
    "clock_period_ns": 10.0
  }'
```

## 🧪 Testing

### Run All Tests
```powershell
.\scripts\test-all.ps1
```

### Run Specific Service Tests
```powershell
cd gateway
pytest tests -v

cd orchestrator
pytest tests -v

cd services\emulator
pytest tests -v
```

### Run Integration Tests
```powershell
cd tests
pip install -r requirements.txt
pytest test_integration.py -v -s
```

## 🔧 Development

### Run Service Locally (Python)
```powershell
cd service-name
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Run Frontend Locally
```powershell
cd frontend
npm install
npm start
```

## 📊 Monitoring

### Check Service Health
```bash
# All services
curl http://localhost:8000/health
curl http://localhost:8001/health
curl http://localhost:8010/health
# ... etc

# Or use the integration test
cd tests
pytest test_integration.py::test_health_checks -v -s
```

### View Container Status
```powershell
docker-compose ps
docker-compose stats
```

### Database Access
```powershell
# PostgreSQL
docker exec -it sparta-postgres psql -U sparta

# Redis
docker exec -it sparta-redis redis-cli
```

## 🐛 Troubleshooting

### Services Won't Start
```powershell
# Check logs
docker-compose logs service-name

# Rebuild containers
docker-compose up -d --build

# Check ports
netstat -an | findstr "8000 8001 3000"
```

### Reset Everything
```powershell
# Stop and remove all containers, volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

### Frontend Issues
```powershell
# Clear Node modules and reinstall
cd frontend
Remove-Item -Recurse -Force node_modules
npm install

# Clear build cache
npm run build -- --clean
```

## 📚 Documentation

- [Architecture](docs/architecture.md) - System design and components
- [API Reference](docs/api-reference.md) - API endpoints and examples
- [Development Guide](docs/development.md) - Development workflow
- [Deployment Guide](docs/deployment.md) - Production deployment
- [Validation Report](VALIDATION_REPORT.md) - Project validation

## 🔑 Default Credentials

- **RabbitMQ**: sparta / sparta_dev_password
- **PostgreSQL**: sparta / sparta_dev_password
- **Database**: sparta

⚠️ **Change these in production!**

## 📦 Project Structure

```
TestProject/
├── frontend/           # React UI
├── gateway/            # API Gateway
├── orchestrator/       # AI Orchestrator
├── agents/             # Specialized agents (4)
├── services/           # Backend services (4)
├── shared/             # Shared schemas
├── tests/              # Integration tests
├── docs/               # Documentation
├── scripts/            # Helper scripts
└── docker-compose.yml  # Service orchestration
```

## 💡 Tips

- Use `docker-compose logs -f service-name` to debug specific services
- Frontend hot-reloads on file changes
- Backend services use `--reload` for auto-restart
- Check `/health` endpoints to verify services are running
- Use Swagger UI at http://localhost:8000/docs for API exploration

## 🎯 Next Steps

1. Start services: `.\scripts\start.ps1`
2. Open frontend: http://localhost:3000
3. Try: "Create a 32-bit adder"
4. Explore API docs: http://localhost:8000/docs
5. Run tests: `.\scripts\test-all.ps1`

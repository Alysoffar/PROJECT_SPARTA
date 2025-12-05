# Development Guide

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.11+
- Node.js 18+
- Git

### Initial Setup

1. Clone the repository
2. Start services:
   ```powershell
   .\scripts\start.ps1
   ```

## Development Workflow

### Backend Services

Each Python service follows the same structure:

```
service-name/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── ...
├── tests/
│   ├── __init__.py
│   └── test_*.py
├── Dockerfile
├── requirements.txt
└── README.md
```

#### Running a Service Locally

```powershell
cd service-name
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

#### Running Tests

```powershell
pip install -r requirements-dev.txt
pytest tests -v
```

### Frontend

```powershell
cd frontend
npm install
npm start
```

Runs on `http://localhost:3000`

### Adding a New Endpoint

1. Create endpoint in `app/main.py` or `app/api/v1/endpoints/`
2. Add request/response models using Pydantic
3. Write tests in `tests/test_*.py`
4. Update API documentation
5. Run tests to verify

### Adding a New Service

1. Create service directory under `services/` or `agents/`
2. Copy structure from existing service
3. Update `docker-compose.yml`
4. Add service URL to orchestrator config
5. Create Dockerfile and requirements.txt
6. Write tests

## Code Standards

### Python

- Use type hints
- Follow PEP 8
- Use Pydantic for data validation
- Write docstrings for all functions
- Minimum 80% test coverage

### TypeScript

- Use strict mode
- Define interfaces for all data structures
- Use functional components
- Follow React best practices

## Testing Strategy

### Unit Tests
- Test individual functions/methods
- Mock external dependencies
- Fast execution

### Integration Tests
- Test service interactions
- Use TestClient for API tests
- Test actual database operations

### End-to-End Tests
- Full workflow testing
- Frontend to backend
- Manual testing scenarios

## Common Tasks

### Adding a New Workflow Stage

1. Add stage to `WorkflowStage` enum in `shared/schemas/orchestration.py`
2. Implement stage logic in `orchestrator/app/workflow_manager.py`
3. Update frontend stage display
4. Add tests

### Modifying Shared Schemas

1. Update schemas in `shared/schemas/`
2. Update TypeScript types in `frontend/src/types/`
3. Ensure consistency across services
4. Update API documentation

## Debugging

### View Logs

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f gateway
```

### Attach to Container

```powershell
docker exec -it sparta-gateway bash
```

### Debug Python Service

Add breakpoint:
```python
import pdb; pdb.set_trace()
```

## Performance Optimization

- Use async/await for I/O operations
- Cache frequently accessed data in Redis
- Use database indexes
- Implement pagination for large datasets
- Profile code with cProfile

## Security Best Practices

- Never commit secrets
- Use environment variables
- Validate all inputs
- Sanitize user data
- Use HTTPS in production

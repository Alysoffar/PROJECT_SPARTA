# API Gateway

FastAPI-based API gateway for SPARTA platform.

## Features

- Request routing to microservices
- Authentication & authorization
- Rate limiting
- Request/response validation
- API versioning
- OpenAPI documentation

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest
```

## Environment Variables

Create `.env`:

```env
DATABASE_URL=postgresql://sparta:sparta_dev_password@localhost:5432/sparta
REDIS_URL=redis://localhost:6379
ORCHESTRATOR_URL=http://localhost:8001
SECRET_KEY=your-secret-key-here
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI spec: http://localhost:8000/openapi.json

## Endpoints

```
POST   /api/v1/workflows          # Create new workflow
GET    /api/v1/workflows/{id}     # Get workflow status
POST   /api/v1/designs             # Submit design request
GET    /api/v1/designs/{id}        # Get design details
POST   /api/v1/emulate             # Run emulation
GET    /api/v1/health              # Health check
```

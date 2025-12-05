# Deployment Guide

## Local Development Deployment

### Using Docker Compose (Recommended)

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

### Services Access

- Frontend: http://localhost:3000
- API Gateway: http://localhost:8000
- Gateway Docs: http://localhost:8000/docs
- Orchestrator: http://localhost:8001
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- RabbitMQ Management: http://localhost:15672

### Manual Service Start

If you need to run services individually:

#### Backend Services (Python)

```powershell
# Gateway
cd gateway
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Orchestrator
cd orchestrator
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001

# Emulator
cd services\emulator
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8020
```

#### Frontend

```powershell
cd frontend
npm install
npm start
```

## Production Deployment

### Kubernetes Deployment

#### Prerequisites

- Kubernetes cluster (1.25+)
- kubectl configured
- Docker registry

#### Deploy Infrastructure

```powershell
# Apply Kubernetes manifests
kubectl apply -f infrastructure/kubernetes/namespace.yaml
kubectl apply -f infrastructure/kubernetes/postgres.yaml
kubectl apply -f infrastructure/kubernetes/redis.yaml
kubectl apply -f infrastructure/kubernetes/rabbitmq.yaml
```

#### Deploy Services

```powershell
# Deploy backend services
kubectl apply -f infrastructure/kubernetes/gateway.yaml
kubectl apply -f infrastructure/kubernetes/orchestrator.yaml
kubectl apply -f infrastructure/kubernetes/agents/
kubectl apply -f infrastructure/kubernetes/services/

# Deploy frontend
kubectl apply -f infrastructure/kubernetes/frontend.yaml
```

#### Verify Deployment

```powershell
# Check pods
kubectl get pods -n sparta

# Check services
kubectl get svc -n sparta

# View logs
kubectl logs -f deployment/sparta-gateway -n sparta
```

### Environment Variables

Create `.env` files for each service:

#### Gateway (.env)
```env
DATABASE_URL=postgresql://user:pass@postgres:5432/sparta
REDIS_URL=redis://redis:6379
ORCHESTRATOR_URL=http://orchestrator:8001
SECRET_KEY=<secure-random-key>
```

#### Orchestrator (.env)
```env
REDIS_URL=redis://redis:6379
RABBITMQ_URL=amqp://user:pass@rabbitmq:5672/
NLP_AGENT_URL=http://nlp-agent:8010
SYNTHESIS_AGENT_URL=http://synthesis-agent:8011
OPTIMIZATION_AGENT_URL=http://optimization-agent:8012
VISUALIZATION_AGENT_URL=http://visualization-agent:8013
EMULATOR_URL=http://emulator:8020
RTL_GENERATOR_URL=http://rtl-generator:8021
MODEL_SYNTHESIS_URL=http://model-synthesis:8022
COMPILER_URL=http://compiler:8023
```

## CI/CD Pipeline

### GitHub Actions

The project includes GitHub Actions workflows for:

- **Build**: Build Docker images
- **Test**: Run unit and integration tests
- **Deploy**: Deploy to Kubernetes

### Manual Build

```powershell
# Build all images
docker-compose build

# Tag for registry
docker tag sparta-gateway your-registry/sparta-gateway:latest

# Push to registry
docker push your-registry/sparta-gateway:latest
```

## Monitoring

### Prometheus + Grafana

```powershell
# Deploy monitoring stack
kubectl apply -f infrastructure/kubernetes/monitoring/
```

Access Grafana: http://grafana.your-domain.com

### Health Checks

All services expose `/health` endpoint for monitoring.

## Troubleshooting

### Services Not Starting

1. Check logs: `docker-compose logs service-name`
2. Verify environment variables
3. Check port conflicts
4. Ensure dependencies are healthy

### Database Connection Issues

1. Verify PostgreSQL is running
2. Check DATABASE_URL format
3. Ensure database exists: `CREATE DATABASE sparta;`
4. Check network connectivity

### Frontend Not Loading

1. Check if gateway is running
2. Verify REACT_APP_API_URL in frontend/.env
3. Check CORS settings in gateway
4. Clear browser cache

## Security

### Production Checklist

- [ ] Change all default passwords
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Enable authentication
- [ ] Set up secrets management
- [ ] Configure rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Backup database regularly

## Scaling

### Horizontal Scaling

```yaml
# In Kubernetes deployment
spec:
  replicas: 3  # Scale to 3 instances
```

### Auto-scaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: sparta-gateway
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: sparta-gateway
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Backup and Recovery

### Database Backup

```powershell
# Backup
docker exec sparta-postgres pg_dump -U sparta sparta > backup.sql

# Restore
docker exec -i sparta-postgres psql -U sparta sparta < backup.sql
```

### Configuration Backup

```powershell
# Backup Kubernetes configs
kubectl get all -n sparta -o yaml > sparta-backup.yaml
```

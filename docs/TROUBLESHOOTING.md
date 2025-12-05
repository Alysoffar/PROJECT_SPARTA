# SPARTA Troubleshooting Guide

## Quick Start Issues

### Docker Desktop Not Found

**Symptom**: `docker: The term 'docker' is not recognized`

**Solution**:
1. Install Docker Desktop from: https://www.docker.com/products/docker-desktop
2. After installation, restart your terminal
3. The `start.ps1` script will now auto-detect and start Docker Desktop

### Docker Desktop Not Running

**Symptom**: Script says "Docker Desktop is not running"

**Solution**: The script will automatically:
- Detect Docker Desktop installation
- Start Docker Desktop if not running
- Wait up to 60 seconds for Docker to be ready

If auto-start fails:
- Manually start Docker Desktop from Start Menu
- Wait for Docker icon in system tray to show "Docker Desktop is running"
- Re-run `.\scripts\start.ps1`

### Services Take Too Long to Start

**Symptom**: Script completes but services show as "starting..."

**Solution**: This is normal! Services can take 1-2 minutes to fully initialize.

- **Infrastructure services** (Postgres, Redis, RabbitMQ) start first
- **Application services** wait for infrastructure to be healthy
- **Check progress**: `docker compose logs -f`

### Integration Tests Fail with ConnectError

**Symptom**: `httpx.ConnectError: [Errno 111] Connection refused`

**Root Causes**:
1. **Services not started**: Run `.\scripts\start.ps1` first
2. **Services still initializing**: Wait 1-2 minutes after start.ps1
3. **Port conflicts**: Another application using ports 8000-8023

**Solution**:
```powershell
# Stop everything
docker compose down

# Check for port conflicts
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

# Restart cleanly
.\scripts\start.ps1

# Wait for "All core services are healthy!" message
# Then run tests
pytest tests\test_integration.py -v
```

### HTTPx Version Conflicts

**Symptom**: `ERROR: Cannot install httpx==0.26.0 and httpx>=0.27.1`

**Solution**: FIXED! Now uses `httpx>=0.27.1` in test requirements.

If you previously installed test dependencies:
```powershell
pip uninstall httpx -y
pip install -r tests\requirements.txt
```

## Service-Specific Issues

### Gateway Won't Start

**Check**:
```powershell
docker compose logs gateway
```

**Common Issues**:
- Database connection failed → Check if postgres container is healthy
- Redis connection failed → Check if redis container is healthy

**Solution**:
```powershell
docker compose restart postgres redis
docker compose restart gateway
```

### Orchestrator Won't Start

**Check**:
```powershell
docker compose logs orchestrator
```

**Common Issues**:
- RabbitMQ connection failed → Check if rabbitmq container is healthy
- Database not ready → Postgres still initializing

**Solution**:
```powershell
docker compose restart rabbitmq postgres
docker compose restart orchestrator
```

### Agent Services Not Responding

**Check**:
```powershell
docker compose ps
docker compose logs nlp-agent synthesis-agent verification-agent planning-agent
```

**Common Issues**:
- ChromaDB initialization taking time
- Waiting for message queue
- Model downloads (first run only)

**Solution**: Just wait. First startup can take 2-3 minutes.

### Frontend Shows API Errors

**Check**:
1. Is Gateway running? `curl http://localhost:8000/health`
2. Are services healthy? `docker compose ps`

**Solution**:
```powershell
# Check gateway specifically
docker compose logs gateway

# Restart frontend and gateway
docker compose restart frontend gateway
```

## Docker Compose Issues

### "docker compose" Command Not Found

**Symptom**: `docker: 'compose' is not a docker command`

**Cause**: Very old Docker Desktop version (< 2.0)

**Solution**:
1. Update Docker Desktop to latest version
2. OR edit `scripts\start.ps1` line 113: change `docker compose` to `docker-compose`

### "docker-compose" Command Not Found

**Symptom**: `docker-compose: The term 'docker-compose' is not recognized`

**Cause**: Docker Desktop v2+ uses `docker compose` (with space), not `docker-compose`

**Solution**: Already fixed in `start.ps1`! Script tries both syntaxes.

### Services Exit Immediately

**Check**:
```powershell
docker compose ps -a
docker compose logs <service-name>
```

**Common Causes**:
- Missing environment variables
- Port already in use
- Database migration failed

**Solution**:
```powershell
# Clean restart
docker compose down -v  # Removes volumes too
.\scripts\start.ps1
```

## Testing Issues

### Tests Skip with "Services not running"

**Symptom**: `SKIPPED - Services are not running`

**Cause**: Tests check if services are healthy before running

**Solution**:
```powershell
# Start services first
.\scripts\start.ps1

# Wait for "All core services are healthy!"
# Then run tests
pytest tests\test_integration.py -v
```

### Tests Timeout

**Symptom**: Tests hang for 60+ seconds then fail

**Cause**: Services overloaded or stuck

**Solution**:
```powershell
# Check service health
docker compose ps

# Check CPU/memory usage
docker stats

# Restart specific service
docker compose restart <service-name>
```

### Test Workflow Never Completes

**Symptom**: `test_end_to_end_workflow` polls for 50+ seconds

**Cause**: Orchestrator or agents not processing tasks

**Debug**:
```powershell
# Check orchestrator
docker compose logs orchestrator

# Check message queue
docker compose logs rabbitmq

# Check agents
docker compose logs nlp-agent synthesis-agent
```

**Solution**: Check logs for errors, restart failing services

## Performance Issues

### Services Use Too Much Memory

**Check**:
```powershell
docker stats --no-stream
```

**Solution**: Limit memory in `docker-compose.yml`:
```yaml
services:
  gateway:
    deploy:
      resources:
        limits:
          memory: 512M
```

### Slow First Startup

**Cause**: Normal! First run includes:
- Docker image builds (~5 minutes)
- Python package installs
- Database initialization
- Model downloads

**Solution**: Be patient. Subsequent starts are much faster (~30 seconds).

## Clean Slate Reset

If all else fails:

```powershell
# Nuclear option - removes EVERYTHING
docker compose down -v --rmi all --remove-orphans

# Remove Python cache
Get-ChildItem -Recurse -Directory __pycache__ | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force

# Fresh start
.\scripts\start.ps1
```

## Getting Help

1. **Check logs**: `docker compose logs -f`
2. **Check service status**: `docker compose ps`
3. **Check resource usage**: `docker stats`
4. **Test connectivity**: `curl http://localhost:8000/health`

## Common Error Messages

| Error | Meaning | Fix |
|-------|---------|-----|
| `Connection refused` | Service not running | Start services with `start.ps1` |
| `Connection timeout` | Service overloaded | Check `docker stats`, restart service |
| `404 Not Found` | Wrong URL/endpoint | Check API docs at `/docs` |
| `500 Internal Server Error` | Service crashed | Check `docker compose logs <service>` |
| `Database connection failed` | Postgres not ready | Wait 30s, or restart postgres |
| `Message broker connection failed` | RabbitMQ not ready | Restart rabbitmq |

## Environment-Specific Notes

### Windows-Specific
- Use PowerShell (not CMD)
- Docker Desktop requires WSL2 on Windows 10/11
- Firewall may block localhost ports - add exception

### Path Issues
- Always use absolute paths in docker-compose volumes
- Use forward slashes `/` even on Windows in Docker paths

### Performance
- WSL2 backend is faster than Hyper-V
- Place project in WSL2 filesystem for best performance
- Allocate at least 4GB RAM to Docker Desktop

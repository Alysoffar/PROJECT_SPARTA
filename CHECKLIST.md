# SPARTA - Pre-Launch Checklist

## ✅ SYSTEM VERIFICATION CHECKLIST

Use this checklist to verify your SPARTA installation before first use.

---

## 📋 Installation Verification

### Step 1: Prerequisites ✓
- [ ] Docker Desktop installed and running
- [ ] PowerShell available
- [ ] 10GB free disk space
- [ ] Ports 3000, 5432, 5672, 6379, 8000-8001, 8010-8013, 8020-8023 available

### Step 2: Project Setup ✓
- [ ] Project cloned/extracted to `d:\WORK\projects\TestProject`
- [ ] All files present (85+ files)
- [ ] `docker-compose.yml` exists in root
- [ ] `scripts\start.ps1` is executable

### Step 3: Service Launch ✓
```powershell
# Run this command
.\scripts\start.ps1

# Verify output shows:
# - "Starting services with Docker Compose..."
# - "Services are starting up!"
# - Access points listed
```

- [ ] Script executed without errors
- [ ] 14 containers starting

### Step 4: Container Health ✓
```powershell
# Check all containers are running
docker-compose ps

# Should show 14 services with "Up" status
```

- [ ] sparta-postgres: Up (healthy)
- [ ] sparta-redis: Up (healthy)
- [ ] sparta-rabbitmq: Up (healthy)
- [ ] sparta-gateway: Up
- [ ] sparta-orchestrator: Up
- [ ] sparta-nlp-agent: Up
- [ ] sparta-synthesis-agent: Up
- [ ] sparta-optimization-agent: Up
- [ ] sparta-visualization-agent: Up
- [ ] sparta-emulator: Up
- [ ] sparta-rtl-generator: Up
- [ ] sparta-model-synthesis: Up
- [ ] sparta-compiler: Up
- [ ] sparta-frontend: Up

### Step 5: Service Health Checks ✓
```powershell
# Test each service health endpoint
curl http://localhost:8000/health  # Gateway
curl http://localhost:8001/health  # Orchestrator
curl http://localhost:8010/health  # NLP Agent
curl http://localhost:8011/health  # Synthesis Agent
curl http://localhost:8012/health  # Optimization Agent
curl http://localhost:8013/health  # Visualization Agent
curl http://localhost:8020/health  # Emulator
curl http://localhost:8021/health  # RTL Generator
curl http://localhost:8022/health  # Model Synthesis
curl http://localhost:8023/health  # Compiler
```

- [ ] All return HTTP 200
- [ ] All return `{"status": "healthy"}`

### Step 6: Frontend Access ✓
```powershell
# Open browser to http://localhost:3000
```

- [ ] Page loads successfully
- [ ] "SPARTA" header visible
- [ ] Chat interface displays
- [ ] Welcome message appears
- [ ] Input box is interactive

### Step 7: API Documentation ✓
```powershell
# Open http://localhost:8000/docs
```

- [ ] Swagger UI loads
- [ ] Endpoints listed under "workflows", "designs", "emulation"
- [ ] Can expand and test endpoints

---

## 🧪 FUNCTIONAL TESTING

### Test 1: Simple Workflow ✓

**Via Frontend:**
1. Open http://localhost:3000
2. Type in chat: "Create a 32-bit adder"
3. Click "Send"

**Expected Results:**
- [ ] Message appears in chat
- [ ] "Workflow started!" response received
- [ ] Workflow ID displayed
- [ ] Status panel appears below chat
- [ ] Progress bar shows 0% → 100%
- [ ] Status changes: pending → running → completed

**Completion Time:** ~8-10 seconds

### Test 2: API Workflow ✓

```powershell
# Create workflow
$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/v1/workflows" -Body '{"user_input":"Test workflow"}' -ContentType "application/json"

# Get workflow ID
$workflowId = $response.workflow_id

# Check status
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/workflows/$workflowId"
```

**Expected Results:**
- [ ] Workflow created successfully
- [ ] Workflow ID returned
- [ ] Status endpoint returns current progress
- [ ] Eventually shows "completed" status

### Test 3: Emulation Service ✓

```powershell
$body = @{
    instructions = @(
        @{opcode="ADD"; operands=@("r1","r2","r3")},
        @{opcode="NOP"; operands=@()}
    )
    num_cycles = 10
    clock_period_ns = 10.0
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Method Post -Uri "http://localhost:8020/emulate" -Body $body -ContentType "application/json"
```

**Expected Results:**
- [ ] Returns emulation_id
- [ ] Status: "completed"
- [ ] cycles_executed: 2
- [ ] outputs array with 2 elements
- [ ] performance_metrics included

### Test 4: RTL Generation ✓

```powershell
$body = @{
    spec = @{type="adder"; datapath_width=32}
    language = "systemverilog"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8021/generate" -Body $body -ContentType "application/json"
```

**Expected Results:**
- [ ] Returns RTL code string
- [ ] Code contains "module adder_design"
- [ ] Contains port definitions
- [ ] Contains register declarations

---

## 🔍 AUTOMATED TEST SUITE

### Run All Tests ✓

```powershell
# Execute test suite
.\scripts\test-all.ps1
```

**Expected Results:**
- [ ] Gateway tests: 3/3 passed (or 2/3 if orchestrator not ready)
- [ ] Orchestrator tests: 3/3 passed
- [ ] Emulator tests: 3/3 passed
- [ ] Final message: "All tests passed! ✓"

### Run Integration Tests ✓

```powershell
cd tests
pip install -r requirements.txt
pytest test_integration.py -v -s
```

**Expected Results:**
- [ ] test_end_to_end_workflow: PASSED
- [ ] test_health_checks: PASSED
- [ ] All services show as healthy

---

## 📊 MONITORING VERIFICATION

### Check Logs ✓

```powershell
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f gateway
```

**Expected Logs:**
- [ ] Gateway: "Starting SPARTA API Gateway"
- [ ] Orchestrator: "Workflow manager initialized"
- [ ] No critical errors visible
- [ ] Services show startup messages

### Database Connectivity ✓

```powershell
# Connect to PostgreSQL
docker exec -it sparta-postgres psql -U sparta

# Inside psql:
\l              # List databases
\c sparta       # Connect to sparta DB
\dt             # List tables (may be empty initially)
\q              # Quit
```

- [ ] Can connect to database
- [ ] sparta database exists

### Redis Connectivity ✓

```powershell
# Connect to Redis
docker exec -it sparta-redis redis-cli

# Inside redis-cli:
ping            # Should return PONG
quit
```

- [ ] Can connect to Redis
- [ ] PING returns PONG

### RabbitMQ UI ✓

```powershell
# Open http://localhost:15672
# Login: sparta / sparta_dev_password
```

- [ ] RabbitMQ management UI loads
- [ ] Can login with credentials
- [ ] Shows 0 connections initially (normal)

---

## 🔧 PERFORMANCE BASELINE

### Response Times ✓

Test and record baseline response times:

- [ ] Gateway health check: < 50ms
- [ ] Workflow creation: < 100ms
- [ ] Workflow status query: < 50ms
- [ ] Emulation (10 cycles): < 100ms
- [ ] RTL generation: < 200ms
- [ ] End-to-end workflow: < 15 seconds

### Resource Usage ✓

```powershell
docker stats --no-stream
```

**Acceptable Ranges:**
- [ ] Total CPU: < 50% (idle)
- [ ] Total Memory: < 4GB
- [ ] No container using > 500MB individually

---

## 📚 DOCUMENTATION VERIFICATION

### Files Present ✓

- [ ] README.md
- [ ] QUICK_REFERENCE.md
- [ ] PROJECT_COMPLETE.md
- [ ] VALIDATION_REPORT.md
- [ ] docs/architecture.md
- [ ] docs/api-reference.md
- [ ] docs/development.md
- [ ] docs/deployment.md

### Content Accuracy ✓

- [ ] All URLs in docs point to localhost
- [ ] Port numbers match actual configuration
- [ ] Code examples are correct
- [ ] Commands are PowerShell-compatible

---

## ⚠️ TROUBLESHOOTING CHECKLIST

If any checks fail, try these steps:

### Services Won't Start
```powershell
docker-compose down -v
docker-compose up -d --build
```

### Port Conflicts
```powershell
# Check what's using ports
netstat -ano | findstr "8000 8001 3000"

# Kill process if needed
taskkill /PID <PID> /F
```

### Frontend Won't Load
```powershell
# Check gateway is running
curl http://localhost:8000/health

# Rebuild frontend
docker-compose up -d --build frontend
```

### Database Issues
```powershell
# Check Postgres logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Complete Reset
```powershell
# Nuclear option - reset everything
docker-compose down -v --remove-orphans
docker system prune -a --volumes
docker-compose up -d
```

---

## ✅ FINAL CHECKLIST

### Before Production Use

- [ ] All verification steps passed
- [ ] Functional tests successful
- [ ] Automated tests passing
- [ ] Monitoring working
- [ ] Documentation reviewed
- [ ] Performance acceptable
- [ ] No critical errors in logs

### Security (If deploying to production)

- [ ] Change default passwords
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Configure firewall
- [ ] Set up authentication
- [ ] Review security guide in docs

---

## 🎉 READY TO USE

If all items are checked, your SPARTA installation is verified and ready!

### Next Steps:
1. Keep services running: `docker-compose up -d`
2. Access frontend: http://localhost:3000
3. Try creating designs
4. Explore API: http://localhost:8000/docs
5. Read documentation in `docs/`

### Support Resources:
- Quick Reference: [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- Troubleshooting: [docs/development.md](docs/development.md)
- Validation Report: [VALIDATION_REPORT.md](VALIDATION_REPORT.md)

---

**System Status**: ✅ VERIFIED AND OPERATIONAL

*Last Updated: November 27, 2025*

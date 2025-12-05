# SPARTA API Reference

## API Gateway Endpoints

Base URL: `http://localhost:8000/api/v1`

### Workflows

#### Create Workflow
```http
POST /workflows
Content-Type: application/json

{
  "user_input": "Create a 32-bit adder with low power consumption",
  "parameters": {},
  "metadata": {}
}
```

**Response:**
```json
{
  "workflow_id": "wf-abc123",
  "status": "pending",
  "current_stage": "parsing",
  "progress_percentage": 0.0,
  "stages_completed": [],
  "started_at": "2025-11-27T10:00:00Z",
  "updated_at": "2025-11-27T10:00:00Z"
}
```

#### Get Workflow Status
```http
GET /workflows/{workflow_id}
```

**Response:**
```json
{
  "workflow_id": "wf-abc123",
  "status": "running",
  "current_stage": "generation",
  "progress_percentage": 50.0,
  "stages_completed": ["parsing", "synthesis"],
  "started_at": "2025-11-27T10:00:00Z",
  "updated_at": "2025-11-27T10:00:30Z"
}
```

#### Cancel Workflow
```http
DELETE /workflows/{workflow_id}
```

### Designs

#### Create Design
```http
POST /designs
Content-Type: application/json

{
  "specification": "32-bit ALU",
  "constraints": {
    "power": "low",
    "area": "minimal"
  }
}
```

### Emulation

#### Run Emulation
```http
POST /emulation
Content-Type: application/json

{
  "instructions": [
    {"opcode": "ADD", "operands": ["r1", "r2", "r3"]},
    {"opcode": "LOAD", "operands": ["r4", "0x100"]}
  ],
  "num_cycles": 1000,
  "clock_period_ns": 10.0
}
```

**Response:**
```json
{
  "emulation_id": "emu-xyz789",
  "status": "completed",
  "cycles_executed": 2,
  "execution_time_ms": 15.3,
  "outputs": [...],
  "performance_metrics": {
    "cycles": 2,
    "frequency_mhz": 100.0,
    "execution_time_us": 20.0,
    "ipc": 1.0
  }
}
```

## Orchestrator Endpoints

Base URL: `http://localhost:8001`

### Workflows

Same as Gateway workflow endpoints, but accessed directly.

## Service Endpoints

### NLP Agent (Port 8010)

#### Parse Text
```http
POST /parse
Content-Type: application/json

{
  "text": "Create a low-power 32-bit adder",
  "context": {}
}
```

### Synthesis Agent (Port 8011)

#### Synthesize Design
```http
POST /synthesize
Content-Type: application/json

{
  "spec": {
    "component": "adder",
    "width": 32
  },
  "constraints": {
    "power": "low"
  }
}
```

### Emulator Service (Port 8020)

#### Run Emulation
```http
POST /emulate
Content-Type: application/json

{
  "instructions": [...],
  "num_cycles": 1000,
  "clock_period_ns": 10.0
}
```

### RTL Generator (Port 8021)

#### Generate RTL
```http
POST /generate
Content-Type: application/json

{
  "spec": {
    "type": "adder",
    "datapath_width": 32
  },
  "language": "systemverilog"
}
```

## Error Responses

All endpoints may return the following error format:

```json
{
  "error": "error_code",
  "message": "Human readable error message",
  "details": {...}
}
```

### Common Status Codes

- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `502 Bad Gateway` - Service unavailable

## Rate Limiting

- 60 requests per minute per IP
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`

## Authentication

Currently, no authentication required for development.
Production will use JWT tokens:

```http
Authorization: Bearer <token>
```

# AI Orchestrator Service

Orchestrates AI agents and backend services to process hardware design workflows.

## Features

- Task decomposition from natural language
- Agent coordination and routing
- Workflow state management
- Service orchestration
- Event-driven architecture

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn app.main:app --reload --port 8001

# Run tests
pytest
```

## Environment Variables

```env
REDIS_URL=redis://localhost:6379
RABBITMQ_URL=amqp://sparta:sparta_dev_password@localhost:5672/
NLP_AGENT_URL=http://localhost:8010
SYNTHESIS_AGENT_URL=http://localhost:8011
OPTIMIZATION_AGENT_URL=http://localhost:8012
VISUALIZATION_AGENT_URL=http://localhost:8013
EMULATOR_URL=http://localhost:8020
RTL_GENERATOR_URL=http://localhost:8021
MODEL_SYNTHESIS_URL=http://localhost:8022
COMPILER_URL=http://localhost:8023
```

## Architecture

```
Orchestrator
├── Workflow Manager    # Manages workflow state and progression
├── Task Scheduler      # Schedules and dispatches tasks
├── Agent Router        # Routes to appropriate agents
├── Service Client      # Communicates with backend services
└── Event Bus           # Publishes workflow events
```

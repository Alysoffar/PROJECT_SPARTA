# Hardware Emulator Service

Cycle-accurate hardware emulation service for SPARTA platform.

## Features

- Cycle-accurate instruction execution
- Configurable clock and memory
- Waveform generation
- Performance metrics collection
- Stateful simulation sessions

## Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8020

# Run tests
pytest
```

## API Endpoints

```
POST   /emulate       # Run emulation
GET    /emulate/{id}  # Get emulation results
POST   /sessions      # Create session
DELETE /sessions/{id} # Destroy session
GET    /health        # Health check
```

## Architecture

```
Emulator
├── Instruction Decoder
├── Execution Engine
├── Memory Model
├── Clock Generator
└── Trace Collector
```

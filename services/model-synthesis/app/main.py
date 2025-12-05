"""Model Synthesis Service main application."""
from fastapi import FastAPI


app = FastAPI(
    title="SPARTA Model Synthesis",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check."""
    return {"service": "Model Synthesis", "status": "healthy"}

"""Visualization Agent main application."""
from fastapi import FastAPI


app = FastAPI(
    title="SPARTA Visualization Agent",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check."""
    return {"service": "Visualization Agent", "status": "healthy"}

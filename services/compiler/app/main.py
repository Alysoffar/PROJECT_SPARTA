"""Compiler Service main application."""
from fastapi import FastAPI


app = FastAPI(
    title="SPARTA Compiler",
    version="0.1.0",
)


@app.get("/health")
async def health_check():
    """Health check."""
    return {"service": "Compiler", "status": "healthy"}

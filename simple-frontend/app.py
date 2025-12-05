import os
from typing import Dict, Any
import asyncio
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx

GATEWAY_URL = os.getenv("GATEWAY_URL", "http://localhost:8000")
API_BASE = f"{GATEWAY_URL}/api/v1"

app = FastAPI(title="SPARTA Simple Frontend")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run", response_class=HTMLResponse)
async def run_workflow(request: Request, user_input: str = Form(...)):
    payload: Dict[str, Any] = {
        "user_input": user_input,
        "parameters": {},
        "metadata": {"source": "simple-frontend"},
    }
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(f"{API_BASE}/workflows", json=payload)
            resp.raise_for_status()
            data = resp.json()
            workflow_id = data.get("workflow_id")
        except httpx.HTTPError as e:
            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "error": f"Failed to create workflow: {str(e)}",
                    "result": None,
                },
            )

        # Poll a few times for result/demo purposes
        status = None
        for _ in range(20):
            s = await client.get(f"{API_BASE}/workflows/{workflow_id}")
            if s.status_code == 200:
                status = s.json()
                if status.get("status") in ("completed", "failed"):
                    break
            await asyncio.sleep(1)

        # Try to fetch detailed result/artifacts if available
        result_data = None
        try:
            r = await client.get(f"{API_BASE}/workflows/{workflow_id}/result")
            if r.status_code == 200:
                result_data = r.json()
        except httpx.HTTPError:
            pass

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "workflow_id": workflow_id,
                "status": status.get("status") if status else "unknown",
                "progress": status.get("progress_percentage") if status else 0,
                "stages": status.get("stages_completed") if status else [],
                "raw": status,
                "result": result_data,
            },
        )
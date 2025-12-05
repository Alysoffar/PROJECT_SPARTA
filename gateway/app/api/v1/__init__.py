"""API v1 router."""
from fastapi import APIRouter

from app.api.v1.endpoints import workflows, designs, emulation


router = APIRouter()

router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
router.include_router(designs.router, prefix="/designs", tags=["designs"])
router.include_router(emulation.router, prefix="/emulation", tags=["emulation"])

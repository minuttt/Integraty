from fastapi import APIRouter

router = APIRouter()

# Import endpoints
from integraty.api.v1.endpoints import sessions

# Include routers
router.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

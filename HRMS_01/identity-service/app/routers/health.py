"""Health check router."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"ping": "pong"}

@router.get("/health")
async def health():
    from app.config import get_settings
    settings = get_settings()
    return {"status": "healthy", "service": settings.service_name}

"""API routers."""
from fastapi import APIRouter
from app.routers import auth, employee, accessibility, ldap, outlook, health, notes, tags, disciplinary, rewards, company

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(employee.router)
api_router.include_router(accessibility.router)
api_router.include_router(ldap.router)
api_router.include_router(outlook.router)
api_router.include_router(notes.router)
api_router.include_router(tags.router)
api_router.include_router(disciplinary.router)
api_router.include_router(rewards.router)
api_router.include_router(company.router)

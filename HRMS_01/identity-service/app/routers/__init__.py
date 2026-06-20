"""API routers."""
from fastapi import APIRouter
from app.routers import auth, employee, accessibility, ldap, outlook, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(employee.router)
api_router.include_router(accessibility.router)
api_router.include_router(ldap.router)
api_router.include_router(outlook.router)

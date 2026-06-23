from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import async_session, init_db
from app.routers import api_router
from seed import seed_permissions

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as db:
        await seed_permissions(db)
    yield

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.service_name, version="1.0.0", docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/openapi.json", root_path="/api/permissions", servers=[{"url": "/api/permissions"}], lifespan=lifespan)
    @app.get("/api/openapi.json", include_in_schema=False)
    async def get_openapi_json():
        from fastapi.responses import JSONResponse
        return JSONResponse(app.openapi())
    @app.middleware("http")
    async def fix_nginx_double_api_prefix(request: Request, call_next):
        if request.scope["path"].startswith("/api/api/"):
            request.scope["path"] = request.scope["path"][4:]
        return await call_next(request)
        
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(api_router, prefix="/api/v1")
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": settings.service_name}
    from horilla_common.exceptions import add_global_exception_handlers
    add_global_exception_handlers(app)

    return app

app = create_app()

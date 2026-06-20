from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import async_session, init_db
from app.routers import api_router
from app.seed import seed_permissions

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async with async_session() as db:
        await seed_permissions(db)
    yield

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.service_name, version="1.0.0", docs_url="/docs", redoc_url="/redoc", lifespan=lifespan)
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
    app.include_router(api_router, prefix="/api/v1")
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": settings.service_name}
    from horilla_common.exceptions import add_global_exception_handlers
    add_global_exception_handlers(app)

    return app

app = create_app()

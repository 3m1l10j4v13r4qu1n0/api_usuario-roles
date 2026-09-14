from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.core.config import settings
from app.presentation.handlers import registrar_handlers
from app.presentation.routers.auth import router as auth_router
from app.presentation.routers.roles import router as roles_router
from app.presentation.routers.usuarios import router as usuarios_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Eventos de inicio y cierre de la aplicación
    Reemplaza el deprecado @app.on_event("startup")
    """
    # ── Inicio ──────────────────────────────────────
    print(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🔧 Modo DEBUG: {settings.DEBUG}")
    yield
    # ── Cierre ──────────────────────────────────────
    print("👋 Cerrando aplicación")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="""
    API REST de autenticación y autorización (JWT) con gestión de usuarios y roles.

    Permite registrar usuarios, autenticarse, asignar roles y gestionar
    el acceso por rol a los servicios del ecosistema.
    """,
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Handlers de errores ──────────────────────────────────────────────
registrar_handlers(app)

# ── Routers ──────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(usuarios_router)
app.include_router(roles_router)


# ── Health check ─────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "estado": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }

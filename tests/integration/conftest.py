"""
Configuración de tests de integración (Fase 4 + Fase 5).

Requieren una BD real PostgreSQL (la del .env de la raíz del repo).
Se excluyen por defecto de `pytest` (addopts --ignore) y se corren con:
    python -m pytest tests/integration/
"""

import asyncio
import os

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

# Quitar DATABASE_URL del entorno para que config.py lea el .env real
os.environ.pop("DATABASE_URL", None)

from fastapi.testclient import TestClient

from app.infrastructure.auth.password_hasher import build_hasher
from app.infrastructure.core.config import settings
from app.main import app

# El engine de la app vive solo dentro del loop del TestClient.
# El ping y la limpieza usan engines propios descartables para no
# compartir conexiones entre event loops distintos.

# Bootstrap del primer ADMIN: se recrea en cada test porque la limpieza
# borra `usuarios`/`usuario_roles`. Necesario para que las pruebas de
# autorización puedan asignar/remover roles (hoy eso exige rol ADMIN).
ADMIN_EMAIL = "admin@bootstrap.com"
ADMIN_PASSWORD = "Admin123!"


@pytest.fixture(scope="session")
def cliente() -> TestClient:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def token_admin(cliente: TestClient) -> str:
    resp = cliente.post(
        "/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )
    assert resp.status_code == 200, resp.text
    return resp.json()["access_token"]


@pytest.fixture(scope="session", autouse=True)
def bd_real_disponible():
    try:
        asyncio.run(_ping())
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"BD real no disponible: {exc}")


@pytest.fixture(autouse=True)
def _limpiar_estado():
    yield
    asyncio.run(_borrar_datos())


async def _ping():
    engine_ping = create_async_engine(settings.DATABASE_URL, echo=False)
    try:
        async with engine_ping.connect() as conn:
            await conn.execute(text("SELECT 1"))
    finally:
        await engine_ping.dispose()


async def _crear_admin_bootstrap(conn) -> None:
    password_hash = build_hasher().hash_password(ADMIN_PASSWORD)
    rol_id = (
        await conn.execute(text("SELECT id FROM roles WHERE nombre = 'ADMIN'"))
    ).scalar_one()
    admin_id = (
        await conn.execute(
            text(
                "INSERT INTO usuarios (nombre_usuario, email, password_hash, activo) "
                "VALUES (:nombre, :email, :hash, true) RETURNING id"
            ),
            {"nombre": "admin_bootstrap", "email": ADMIN_EMAIL, "hash": password_hash},
        )
    ).scalar_one()
    await conn.execute(
        text("INSERT INTO usuario_roles (usuario_id, rol_id) VALUES (:usuario, :rol)"),
        {"usuario": admin_id, "rol": rol_id},
    )


async def _borrar_datos():
    engine_limpieza = create_async_engine(settings.DATABASE_URL, echo=False)
    try:
        async with engine_limpieza.begin() as conn:
            await conn.execute(text("DELETE FROM usuario_roles"))
            await conn.execute(text("DELETE FROM usuarios"))
            await conn.execute(
                text("DELETE FROM roles WHERE nombre NOT IN ('ADMIN', 'USUARIO')")
            )
            await _crear_admin_bootstrap(conn)
    finally:
        await engine_limpieza.dispose()

"""
Configuración de tests de integración (Fase 4).

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

from app.infrastructure.core.config import settings
from app.main import app

# El engine de la app vive solo dentro del loop del TestClient.
# El ping y la limpieza usan engines propios descartables para no
# compartir conexiones entre event loops distintos.


@pytest.fixture(scope="session")
def cliente() -> TestClient:
    with TestClient(app) as c:
        yield c


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


async def _borrar_datos():
    engine_limpieza = create_async_engine(settings.DATABASE_URL, echo=False)
    try:
        async with engine_limpieza.begin() as conn:
            await conn.execute(text("DELETE FROM usuario_roles"))
            await conn.execute(text("DELETE FROM usuarios"))
            await conn.execute(
                text("DELETE FROM roles WHERE nombre NOT IN ('ADMIN', 'USUARIO')")
            )
    finally:
        await engine_limpieza.dispose()

#!/bin/sh
set -e

echo "🌀 Esperando conexión a la base de datos..."
python - <<'PY'
import asyncio
import sys

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.infrastructure.core.config import settings


async def esperar_base() -> None:
    engine = create_async_engine(settings.DATABASE_URL)
    for intento in range(30):
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            await engine.dispose()
            print("✅ Base de datos disponible")
            return
        except Exception:
            await engine.dispose()
            await asyncio.sleep(2)
    print("❌ No se pudo conectar a la base de datos", file=sys.stderr)
    sys.exit(1)


asyncio.run(esperar_base())
PY

echo "🧬 Aplicando migraciones..."
alembic upgrade head

echo "🌱 Cargando datos iniciales..."
python -m app.infrastructure.database.seed_runner

echo "🚀 Iniciando uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8001
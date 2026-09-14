from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.infrastructure.core.config import settings  # ← reemplaza os.getenv

# Motor de conexión a PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,  # ← viene de config.py
    echo=settings.DEBUG,  # ← True en desarrollo, False en producción
    future=True,
)

# Fábrica de sesiones
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


# Base para los modelos ORM
class Base(DeclarativeBase):
    pass


# Dependencia para los endpoints
async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

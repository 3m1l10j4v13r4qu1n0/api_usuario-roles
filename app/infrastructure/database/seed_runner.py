import asyncio

from app.infrastructure.database.connection import AsyncSessionLocal
from app.infrastructure.database.seed import cargar_datos_iniciales


async def main():
    print("Iniciando carga de datos iniciales...")
    async with AsyncSessionLocal() as db:
        await cargar_datos_iniciales(db)
    print("Proceso finalizado")


if __name__ == "__main__":
    asyncio.run(main())

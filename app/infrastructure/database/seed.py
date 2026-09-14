from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database.orm_models.rol_orm import RolORM


async def cargar_si_vacia(db: AsyncSession, modelo, datos: list):
    """Inserta datos solo si la tabla está vacía — evita duplicados"""

    resultado = await db.execute(select(modelo))

    if resultado.scalars().first() is None:
        for item in datos:
            db.add(item)
        await db.commit()
        print(f"✅ {modelo.__tablename__} cargada")
    else:
        print(f"⏭️  {modelo.__tablename__} ya tiene datos, se omite")


async def cargar_datos_iniciales(db: AsyncSession):

    await cargar_si_vacia(
        db,
        RolORM,
        [
            RolORM(nombre="ADMIN", descripcion="Acceso total al sistema"),
            RolORM(nombre="USUARIO", descripcion="Acceso básico al sistema"),
        ],
    )

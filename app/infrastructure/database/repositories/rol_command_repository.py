from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.rol import Rol
from app.domain.ports.rol.rol_command_port import RolCommandPort
from app.infrastructure.database.orm_models.rol_orm import RolORM


def _rol_orm_a_entidad(orm: RolORM) -> Rol:
    return Rol(
        id=orm.id,
        nombre=orm.nombre,
        descripcion=orm.descripcion,
    )


class RolCommandRepository(RolCommandPort):
    """
    Implementación de escritura de roles con SQLAlchemy async.
    La sesión se inyecta desde el contenedor de dependencias.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def crear(self, rol: Rol) -> Rol:
        orm = RolORM(nombre=rol.nombre, descripcion=rol.descripcion)
        self._session.add(orm)
        await self._session.flush()
        return _rol_orm_a_entidad(orm)

    async def buscar_por_id(self, rol_id: int) -> Rol | None:
        orm = await self._session.get(RolORM, rol_id)
        return _rol_orm_a_entidad(orm) if orm else None

    async def buscar_por_nombre(self, nombre: str) -> Rol | None:
        resultado = await self._session.execute(
            select(RolORM).where(RolORM.nombre == nombre)
        )
        orm = resultado.scalar_one_or_none()
        return _rol_orm_a_entidad(orm) if orm else None

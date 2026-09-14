from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models.rol import Rol
from app.domain.ports.rol.rol_query_port import RolQueryPort
from app.infrastructure.database.orm_models.rol_orm import RolORM
from app.infrastructure.database.repositories.rol_command_repository import (
    _rol_orm_a_entidad,
)


class RolQueryRepository(RolQueryPort):
    """
    Implementación de consultas de roles con SQLAlchemy async.
    La sesión se inyecta desde el contenedor de dependencias.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def listar(self) -> list[Rol]:
        resultado = await self._session.execute(select(RolORM))
        orms = resultado.scalars().all()
        return [_rol_orm_a_entidad(orm) for orm in orms]

    async def obtener_nombres_por_ids(self, ids_roles: list[int]) -> list[str]:
        if not ids_roles:
            return []

        resultado = await self._session.execute(
            select(RolORM).where(RolORM.id.in_(ids_roles))
        )
        roles = resultado.scalars().all()
        return [rol.nombre for rol in roles]

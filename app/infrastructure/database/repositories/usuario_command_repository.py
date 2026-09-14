from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.models.usuario import Usuario
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort
from app.infrastructure.database.orm_models.rol_orm import RolORM
from app.infrastructure.database.orm_models.usuario_orm import UsuarioORM
from app.infrastructure.database.repositories.usuario_query_repository import (
    _usuario_orm_a_entidad,
)


async def _refresh_con_roles(session: AsyncSession, orm: UsuarioORM) -> None:
    await session.refresh(orm, ["roles"])


def _query_con_roles_email(email: str):
    return (
        select(UsuarioORM)
        .options(selectinload(UsuarioORM.roles))
        .where(UsuarioORM.email == email)
    )


def _query_con_roles_email_excluyendo(email: str, usuario_id: int):
    return (
        select(UsuarioORM)
        .options(selectinload(UsuarioORM.roles))
        .where(UsuarioORM.email == email, UsuarioORM.id != usuario_id)
    )


class UsuarioCommandRepository(UsuarioCommandPort):
    """
    Implementación de escritura de usuarios con SQLAlchemy async.
    La sesión se inyecta desde el contenedor de dependencias.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def crear(self, usuario: Usuario) -> Usuario:
        orm = UsuarioORM(
            nombre_usuario=usuario.nombre_usuario,
            email=usuario.email,
            password_hash=usuario.password_hash,
            nombre_completo=usuario.nombre_completo,
            activo=usuario.activo,
        )
        self._session.add(orm)
        await self._session.flush()
        await _refresh_con_roles(self._session, orm)
        return _usuario_orm_a_entidad(orm)

    async def actualizar(self, usuario_id: int, campos: dict) -> Usuario | None:
        orm = await self._session.get(UsuarioORM, usuario_id)
        if orm is None:
            return None

        for campo, valor in campos.items():
            if hasattr(orm, campo) and campo != "id":
                setattr(orm, campo, valor)

        await self._session.flush()
        await _refresh_con_roles(self._session, orm)
        return _usuario_orm_a_entidad(orm)

    async def dar_de_baja(self, usuario_id: int) -> Usuario | None:
        orm = await self._session.get(UsuarioORM, usuario_id)
        if orm is None:
            return None

        orm.activo = False
        await self._session.flush()
        await _refresh_con_roles(self._session, orm)
        return _usuario_orm_a_entidad(orm)

    async def asignar_rol(self, usuario_id: int, rol_id: int) -> Usuario | None:
        orm = await self._session.get(UsuarioORM, usuario_id)
        if orm is None:
            return None

        rol_orm = await self._session.get(RolORM, rol_id)
        if rol_orm is not None and rol_orm not in orm.roles:
            orm.roles.append(rol_orm)

        await self._session.flush()
        await _refresh_con_roles(self._session, orm)
        return _usuario_orm_a_entidad(orm)

    async def buscar_por_email(self, email: str) -> Usuario | None:
        resultado = await self._session.execute(_query_con_roles_email(email))
        orm = resultado.scalar_one_or_none()
        return _usuario_orm_a_entidad(orm) if orm else None

    async def buscar_por_email_excluyendo_id(
        self, email: str, usuario_id: int
    ) -> Usuario | None:
        resultado = await self._session.execute(
            _query_con_roles_email_excluyendo(email, usuario_id)
        )
        orm = resultado.scalar_one_or_none()
        return _usuario_orm_a_entidad(orm) if orm else None

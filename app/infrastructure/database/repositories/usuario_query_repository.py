from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.models.usuario import Usuario
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort
from app.infrastructure.database.orm_models.usuario_orm import UsuarioORM


def _usuario_orm_a_entidad(orm: UsuarioORM) -> Usuario:
    return Usuario(
        id=orm.id,
        nombre_usuario=orm.nombre_usuario,
        email=orm.email,
        password_hash=orm.password_hash,
        nombre_completo=orm.nombre_completo,
        activo=orm.activo,
        fecha_creacion=orm.fecha_creacion,
        fecha_actualizacion=orm.fecha_actualizacion,
        ids_roles=[rol.id for rol in orm.roles],
    )


def _query_con_roles():
    return select(UsuarioORM).options(selectinload(UsuarioORM.roles))


class UsuarioQueryRepository(UsuarioQueryPort):
    """
    Implementación de consultas de usuarios con SQLAlchemy async.
    La sesión se inyecta desde el contenedor de dependencias.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def listar(self) -> list[Usuario]:
        resultado = await self._session.execute(_query_con_roles())
        orms = resultado.scalars().all()
        return [_usuario_orm_a_entidad(orm) for orm in orms]

    async def obtener_por_id(self, usuario_id: int) -> Usuario | None:
        resultado = await self._session.execute(
            _query_con_roles().where(UsuarioORM.id == usuario_id)
        )
        orm = resultado.scalar_one_or_none()
        return _usuario_orm_a_entidad(orm) if orm else None

    async def obtener_por_email(self, email: str) -> Usuario | None:
        resultado = await self._session.execute(
            _query_con_roles().where(UsuarioORM.email == email)
        )
        orm = resultado.scalar_one_or_none()
        return _usuario_orm_a_entidad(orm) if orm else None

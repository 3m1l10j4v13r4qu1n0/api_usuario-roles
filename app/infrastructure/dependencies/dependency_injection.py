from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.uc1_login import LoginUseCase
from app.application.use_cases.uc2_registrar_usuario import RegistrarUsuarioUseCase
from app.application.use_cases.uc3_listar_usuarios import ListarUsuariosUseCase
from app.application.use_cases.uc4_obtener_usuario_por_id import (
    ObtenerUsuarioPorIdUseCase,
)
from app.application.use_cases.uc5_actualizar_usuario import ActualizarUsuarioUseCase
from app.application.use_cases.uc6_dar_de_baja_usuario import DarDeBajaUsuarioUseCase
from app.application.use_cases.uc7_crear_rol import CrearRolUseCase
from app.application.use_cases.uc8_listar_roles import ListarRolesUseCase
from app.application.use_cases.uc9_asignar_rol import AsignarRolUseCase
from app.application.use_cases.uc10_quitar_rol import QuitarRolUseCase
from app.domain.ports.authentication.estado_usuario_cache_port import (
    EstadoUsuarioCachePort,
)
from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort
from app.domain.ports.authentication.token_provider_port import TokenProviderPort
from app.domain.ports.rol.rol_command_port import RolCommandPort
from app.domain.ports.rol.rol_query_port import RolQueryPort
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort
from app.infrastructure.auth.jwt_token_provider import JwtTokenProvider
from app.infrastructure.auth.password_hasher import build_hasher
from app.infrastructure.cache.estado_usuario_cache_memoria import (
    EstadoUsuarioCacheMemoria,
)
from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.rol_command_repository import (
    RolCommandRepository,
)
from app.infrastructure.database.repositories.rol_query_repository import (
    RolQueryRepository,
)
from app.infrastructure.database.repositories.usuario_command_repository import (
    UsuarioCommandRepository,
)
from app.infrastructure.database.repositories.usuario_query_repository import (
    UsuarioQueryRepository,
)


# ── Auth (singleton) ─────────────────────────────────────────────────
def get_hasher() -> PasswordHasherPort:
    return build_hasher()


def get_token_provider() -> TokenProviderPort:
    return JwtTokenProvider()


def get_estado_usuario_cache() -> EstadoUsuarioCachePort:
    return EstadoUsuarioCacheMemoria()


# ── Repositorios (por request) ───────────────────────────────────────
def get_usuario_query_repo(
    session: AsyncSession = Depends(get_db),
) -> UsuarioQueryPort:
    return UsuarioQueryRepository(session)


def get_usuario_command_repo(
    session: AsyncSession = Depends(get_db),
) -> UsuarioCommandPort:
    return UsuarioCommandRepository(session)


def get_rol_query_repo(
    session: AsyncSession = Depends(get_db),
) -> RolQueryPort:
    return RolQueryRepository(session)


def get_rol_command_repo(
    session: AsyncSession = Depends(get_db),
) -> RolCommandPort:
    return RolCommandRepository(session)


# ── UC1 — Login ──────────────────────────────────────────────────────
def get_login_uc1(
    usuario_repo: UsuarioQueryPort = Depends(get_usuario_query_repo),
    rol_repo: RolQueryPort = Depends(get_rol_query_repo),
    hasher: PasswordHasherPort = Depends(get_hasher),
    token_provider: TokenProviderPort = Depends(get_token_provider),
) -> LoginUseCase:
    return LoginUseCase(
        usuario_repo=usuario_repo,
        rol_repo=rol_repo,
        hasher=hasher,
        token_provider=token_provider,
    )


# ── UC2 — Registrar usuario ──────────────────────────────────────────
def get_registrar_usuario_uc2(
    repo: UsuarioCommandPort = Depends(get_usuario_command_repo),
    rol_repo: RolCommandPort = Depends(get_rol_command_repo),
    hasher: PasswordHasherPort = Depends(get_hasher),
) -> RegistrarUsuarioUseCase:
    return RegistrarUsuarioUseCase(repo, rol_repo, hasher)


# ── UC3 — Listar usuarios ────────────────────────────────────────────
def get_listar_usuarios_uc3(
    repo: UsuarioQueryPort = Depends(get_usuario_query_repo),
) -> ListarUsuariosUseCase:
    return ListarUsuariosUseCase(repo)


# ── UC4 — Obtener usuario por id ─────────────────────────────────────
def get_obtener_usuario_por_id_uc4(
    repo: UsuarioQueryPort = Depends(get_usuario_query_repo),
) -> ObtenerUsuarioPorIdUseCase:
    return ObtenerUsuarioPorIdUseCase(repo)


# ── UC5 — Actualizar usuario ─────────────────────────────────────────
def get_actualizar_usuario_uc5(
    repo: UsuarioCommandPort = Depends(get_usuario_command_repo),
    hasher: PasswordHasherPort = Depends(get_hasher),
) -> ActualizarUsuarioUseCase:
    return ActualizarUsuarioUseCase(repo, hasher)


# ── UC6 — Dar de baja usuario ────────────────────────────────────────
def get_dar_de_baja_usuario_uc6(
    repo: UsuarioCommandPort = Depends(get_usuario_command_repo),
    estado_cache: EstadoUsuarioCachePort = Depends(get_estado_usuario_cache),
) -> DarDeBajaUsuarioUseCase:
    return DarDeBajaUsuarioUseCase(repo, estado_cache)


# ── UC7 — Crear rol ──────────────────────────────────────────────────
def get_crear_rol_uc7(
    repo: RolCommandPort = Depends(get_rol_command_repo),
) -> CrearRolUseCase:
    return CrearRolUseCase(repo)


# ── UC8 — Listar roles ───────────────────────────────────────────────
def get_listar_roles_uc8(
    repo: RolQueryPort = Depends(get_rol_query_repo),
) -> ListarRolesUseCase:
    return ListarRolesUseCase(repo)


# ── UC9 — Asignar rol ────────────────────────────────────────────────
def get_asignar_rol_uc9(
    usuario_repo: UsuarioCommandPort = Depends(get_usuario_command_repo),
    rol_repo: RolCommandPort = Depends(get_rol_command_repo),
    estado_cache: EstadoUsuarioCachePort = Depends(get_estado_usuario_cache),
) -> AsignarRolUseCase:
    return AsignarRolUseCase(usuario_repo, rol_repo, estado_cache)


# ── UC10 — Quitar rol ────────────────────────────────────────────────
def get_quitar_rol_uc10(
    usuario_repo: UsuarioCommandPort = Depends(get_usuario_command_repo),
    rol_repo: RolCommandPort = Depends(get_rol_command_repo),
    estado_cache: EstadoUsuarioCachePort = Depends(get_estado_usuario_cache),
) -> QuitarRolUseCase:
    return QuitarRolUseCase(usuario_repo, rol_repo, estado_cache)

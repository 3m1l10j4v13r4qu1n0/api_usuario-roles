from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.exceptions import NoAutorizadoError, TokenInvalidoError
from app.domain.models.estado_usuario import EstadoUsuario
from app.domain.ports.authentication.estado_usuario_cache_port import (
    EstadoUsuarioCachePort,
)
from app.domain.ports.authentication.token_provider_port import TokenProviderPort
from app.domain.ports.rol.rol_query_port import RolQueryPort
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort
from app.domain.services.auth_service import autorizar
from app.infrastructure.dependencies.dependency_injection import (
    get_estado_usuario_cache,
    get_rol_query_repo,
    get_token_provider,
    get_usuario_query_repo,
)

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_provider: TokenProviderPort = Depends(get_token_provider),
    usuario_repo: UsuarioQueryPort = Depends(get_usuario_query_repo),
    rol_repo: RolQueryPort = Depends(get_rol_query_repo),
    estado_cache: EstadoUsuarioCachePort = Depends(get_estado_usuario_cache),
) -> dict:
    """
    Dependencia que protege un endpoint: exige un Bearer token JWT válido
    y devuelve el usuario autenticado con su estado real.

    Patrón híbrido: decodifica el token (identidad) y resuelve el estado
    (activo + roles) desde el cache de TTL corto; si hay miss, lo carga
    desde la BD y lo guarda en cache. Así la revocación de rol/baja se
    refleja en el próximo request sin esperar la expiración del JWT.

    Raises:
        TokenInvalidoError — Si falta el token, es inválido, está vencido,
            el usuario ya no existe o está inactivo.
    """
    if credentials is None:
        raise TokenInvalidoError()

    payload = token_provider.decodificar_token(credentials.credentials)
    try:
        usuario_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise TokenInvalidoError()

    estado = await estado_cache.obtener(usuario_id)

    if estado is None:
        usuario = await usuario_repo.obtener_por_id(usuario_id)
        if usuario is None:
            raise TokenInvalidoError()

        nombre_roles = await rol_repo.obtener_nombres_por_ids(usuario.ids_roles)
        estado = EstadoUsuario(
            usuario_id=usuario.id,
            email=usuario.email,
            nombre_usuario=usuario.nombre_usuario,
            activo=usuario.activo,
            roles=nombre_roles,
        )
        await estado_cache.guardar(estado)

    if not estado.activo:
        raise TokenInvalidoError()

    return {
        "id": estado.usuario_id,
        "email": estado.email,
        "nombre_usuario": estado.nombre_usuario,
        "roles": estado.roles,
    }


def require_roles(*roles_requeridos: str):
    """
    Fábrica de dependencias de autorización por rol.

    Uso: `Depends(require_roles("ADMIN"))`.

    Raises:
        NoAutorizadoError — Si el usuario autenticado no posee ningún rol
            de los requeridos.
    """

    async def check_roles(
        usuario_actual: dict = Depends(get_current_user),
    ) -> dict:
        autorizar(usuario_actual.get("roles", []), list(roles_requeridos))
        return usuario_actual

    return check_roles


def require_mismo_usuario_o_admin(
    usuario_id: int,
    usuario_actual: dict = Depends(get_current_user),
) -> dict:
    """
    Dependencia de autorización por recurso: permite la operación solo si el
    usuario autenticado es el dueño del recurso (mismo `id`) o tiene rol ADMIN.

    Uso: `Depends(require_mismo_usuario_o_admin)` en endpoints con path
    parameter `usuario_id`.

    Raises:
        NoAutorizadoError — Si el usuario no es el propio recurso ni ADMIN.
    """
    roles = usuario_actual.get("roles", [])
    if "ADMIN" in roles:
        return usuario_actual
    if usuario_id == usuario_actual.get("id"):
        return usuario_actual
    raise NoAutorizadoError()

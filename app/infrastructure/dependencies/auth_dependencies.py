from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.domain.exceptions import TokenInvalidoError
from app.domain.ports.authentication.token_provider_port import TokenProviderPort
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort
from app.domain.services.auth_service import autorizar
from app.infrastructure.dependencies.dependency_injection import (
    get_token_provider,
    get_usuario_query_repo,
)

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    token_provider: TokenProviderPort = Depends(get_token_provider),
    usuario_repo: UsuarioQueryPort = Depends(get_usuario_query_repo),
) -> dict:
    """
    Dependencia que protege un endpoint: exige un Bearer token JWT válido
    y devuelve el usuario autenticado.

    Raises:
        TokenInvalidoError — Si falta el token, es inválido, está vencido
            o el usuario ya no existe.
    """
    if credentials is None:
        raise TokenInvalidoError()

    payload = token_provider.decodificar_token(credentials.credentials)
    try:
        usuario_id = int(payload.get("sub"))
    except (TypeError, ValueError):
        raise TokenInvalidoError()

    usuario = await usuario_repo.obtener_por_id(usuario_id)
    if usuario is None:
        raise TokenInvalidoError()

    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre_usuario": usuario.nombre_usuario,
        "roles": list(payload.get("roles", [])),
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

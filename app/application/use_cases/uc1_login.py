from app.domain.models.usuario import Usuario
from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort
from app.domain.ports.authentication.token_provider_port import TokenProviderPort
from app.domain.ports.rol.rol_query_port import RolQueryPort
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort
from app.domain.services.auth_service import verificar_credenciales
from app.domain.services.normalizacion import normalizar_email

"""
UC1 — Login
Autentica un usuario por email y contraseña y emite un token JWT.
"""


class LoginUseCase:
    """
    UC1 — Valida credenciales y genera el token de acceso.

    Attributes:
        _usuario_repo : UsuarioQueryPort
        _rol_repo : RolQueryPort
        _hasher : PasswordHasherPort
        _token_provider : TokenProviderPort
    """

    def __init__(
        self,
        usuario_repo: UsuarioQueryPort,
        rol_repo: RolQueryPort,
        hasher: PasswordHasherPort,
        token_provider: TokenProviderPort,
    ) -> None:
        self._usuario_repo = usuario_repo
        self._rol_repo = rol_repo
        self._hasher = hasher
        self._token_provider = token_provider

    async def execute(self, email: str, password: str) -> dict:
        """
        Returns:
            dict — Datos de sesión: `access_token`, `token_type`, `id`,
            `email`, `nombre_usuario`, `roles`.

        Raises:
            CredencialesInvalidasError — Si email/password no coinciden
                o el usuario está inactivo.
        """
        email_normalizado = normalizar_email(email)
        usuario_almacenado = await self._usuario_repo.obtener_por_email(
            email_normalizado
        )

        usuario: Usuario = verificar_credenciales(
            usuario_almacenado,
            password,
            self._hasher,
        )

        nombre_roles = await self._rol_repo.obtener_nombres_por_ids(usuario.ids_roles)
        token = self._token_provider.crear_token(usuario.id, nombre_roles)

        return {
            "access_token": token,
            "token_type": "bearer",
            "id": usuario.id,
            "email": usuario.email,
            "nombre_usuario": usuario.nombre_usuario,
            "roles": nombre_roles,
        }

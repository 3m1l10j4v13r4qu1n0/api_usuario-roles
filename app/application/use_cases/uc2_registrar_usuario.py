from app.domain.exceptions import EmailDuplicadoError
from app.domain.models.usuario import Usuario
from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort
from app.domain.services.normalizacion import normalizar_nombre_usuario
from app.domain.services.validacion import (
    normalizar_y_validar_email,
    validar_nombre_usuario,
    validar_password,
)

"""
UC2 — Registrar usuario
Crea un usuario nuevo. Nunca almacena la contraseña en texto plano.
"""


class RegistrarUsuarioUseCase:
    """
    UC2 — Registra un usuario con su contraseña hasheada.

    Attributes:
        _repo : UsuarioCommandPort
        _hasher : PasswordHasherPort
    """

    def __init__(
        self,
        repo: UsuarioCommandPort,
        hasher: PasswordHasherPort,
    ) -> None:
        self._repo = repo
        self._hasher = hasher

    async def execute(self, datos: dict):
        """
        Parámetros:
            datos : dict — `nombre_usuario`, `email`, `password`,
                `nombre_completo` (opcional).

        Raises:
            DatoInvalidoError — Validación de campos o rol.
            EmailDuplicadoError — Si el email ya está registrado.
        """
        email_normalizado = normalizar_y_validar_email(datos.get("email"))
        nombre_usuario = normalizar_nombre_usuario(datos.get("nombre_usuario"))
        validar_nombre_usuario(nombre_usuario)
        validar_password(datos.get("password"))

        existente = await self._repo.buscar_por_email(email_normalizado)
        if existente is not None:
            raise EmailDuplicadoError(email_normalizado)

        password_hash = self._hasher.hash_password(datos["password"])

        usuario = Usuario(
            nombre_usuario=nombre_usuario,
            email=email_normalizado,
            password_hash=password_hash,
            nombre_completo=datos.get("nombre_completo"),
        )

        return await self._repo.crear(usuario)

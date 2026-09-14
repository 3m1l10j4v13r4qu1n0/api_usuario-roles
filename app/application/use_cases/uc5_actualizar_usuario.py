from app.domain.exceptions import EmailDuplicadoError, UsuarioNoEncontradoError
from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort
from app.domain.ports.usuario.usuario_command_port import UsuarioCommandPort
from app.domain.services.validacion import (
    normalizar_y_validar_email,
    validar_password,
)

"""
UC5 — Actualizar usuario
Solo modifica los campos que llegaron en el request.
"""


class ActualizarUsuarioUseCase:
    """
    UC5 — Actualiza los datos de un usuario existente.

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

    async def execute(self, usuario_id: int, datos):
        """
        Raises:
            EmailDuplicadoError — Si el email viene y está en uso por otro.
            UsuarioNoEncontradoError — Si el usuario no existe.
        """
        campos = datos.model_dump(exclude_unset=True)

        # Paso 1 — Normalizar y verificar email si viene
        if "email" in campos:
            email_normalizado = normalizar_y_validar_email(campos["email"])
            campos["email"] = email_normalizado
            en_uso = await self._repo.buscar_por_email_excluyendo_id(
                email=email_normalizado,
                usuario_id=usuario_id,
            )
            if en_uso is not None:
                raise EmailDuplicadoError(email_normalizado)

        # Paso 2 — Hashear la contraseña si viene
        if "password" in campos:
            validar_password(campos["password"])
            campos["password_hash"] = self._hasher.hash_password(campos["password"])
            del campos["password"]

        # Paso 3 — Actualizar y verificar existencia
        usuario = await self._repo.actualizar(usuario_id, campos)

        if usuario is None:
            raise UsuarioNoEncontradoError(f"No existe usuario con id={usuario_id}")

        return usuario

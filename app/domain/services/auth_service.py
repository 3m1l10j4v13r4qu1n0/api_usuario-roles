"""
Servicio de dominio para autenticación y autorización.

Lógica pura: nunca toca bcrypt, PyJWT ni la BD. Recibe
los ports (`PasswordHasherPort`) como dependencia.

UC1 — Login
Autorización por rol de endpoints protegidos
"""

from app.domain.exceptions import CredencialesInvalidasError, NoAutorizadoError
from app.domain.models.usuario import Usuario
from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort


def verificar_password(
    password_plano: str,
    password_hash: str,
    hasher: PasswordHasherPort,
) -> None:
    """UC1 — Verifica que la contraseña corresponda al hash almacenado."""
    if not hasher.verify_password(password_plano, password_hash):
        raise CredencialesInvalidasError()


def verificar_activo(usuario: Usuario) -> None:
    """UC1 — Rechaza usuarios dados de baja (baja lógica)."""
    if not usuario.activo:
        raise CredencialesInvalidasError("El usuario está inactivo")


def verificar_credenciales(
    usuario: Usuario | None,
    password_plano: str,
    hasher: PasswordHasherPort,
) -> Usuario:
    """
    UC1 — Orquesta la verificación de credenciales.

    Raises:
        CredencialesInvalidasError — Si el usuario no existe, está inactivo
            o la contraseña no coincide. Siempre el mismo mensaje genérico
            para no filtrar qué dato fue el incorrecto.
    """
    if usuario is None:
        raise CredencialesInvalidasError()

    verificar_activo(usuario)
    verificar_password(password_plano, usuario.password_hash, hasher)
    return usuario


def autorizar(roles_usuario: list[str], roles_requeridos: list[str]) -> None:
    """
    Autorización por rol: el usuario debe tener ALGUNO de los roles requeridos.
    Si roles_requeridos está vacío, se permite (endpoint con autenticación
    pero sin restricción de rol).

    Raises:
        NoAutorizadoError — Si el usuario no posee ningún rol requerido.
    """
    if not roles_requeridos:
        return

    if not set(roles_requeridos).intersection(roles_usuario):
        raise NoAutorizadoError()

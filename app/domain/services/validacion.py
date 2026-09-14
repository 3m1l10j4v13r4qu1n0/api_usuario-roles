"""
Reglas de validación
RN04 — El email debe tener un formato válido
RN05 — Los campos obligatorios no pueden estar vacíos
RN06 — La contraseña debe tener un largo mínimo de 8 caracteres

"""

from email_validator import EmailNotValidError, validate_email

from app.domain.exceptions import DatoInvalidoError
from app.domain.services.normalizacion import normalizar_email


def validar_email(email: str | None) -> None:
    """RN04 — El email debe tener un formato válido"""
    if not email or not email.strip():
        raise DatoInvalidoError("El email es obligatorio")

    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError as e:
        raise DatoInvalidoError(f"El email '{email}' no es válido: {e!s}")


def validar_nombre_usuario(nombre_usuario: str | None) -> None:
    """RN05 — Los campos obligatorios no pueden estar vacíos"""
    if not nombre_usuario or not nombre_usuario.strip():
        raise DatoInvalidoError("El nombre de usuario es obligatorio")


def validar_password(password: str | None) -> None:
    """
    RN06 — La contraseña debe tener un largo mínimo de 8 caracteres
    RN05 — La contraseña no puede estar vacía
    """
    if not password or not password.strip():
        raise DatoInvalidoError("La contraseña es obligatoria")
    if len(password) < 8:
        raise DatoInvalidoError("La contraseña debe tener al menos 8 caracteres")


def normalizar_y_validar_email(email: str | None) -> str | None:
    """Normaliza (RN01) y valida (RN04) un email, devolviéndolo normalizado."""
    email_normalizado = normalizar_email(email)
    validar_email(email_normalizado)
    return email_normalizado

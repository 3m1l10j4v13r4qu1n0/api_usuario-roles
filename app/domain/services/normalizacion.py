"""
Reglas de normalización
RN01 — Los emails se almacenan en minúsculas
RN02 — Los textos no deben contener espacios al inicio ni al final
RN03 — Los nombres de usuario son sensibles a mayúsculas (se conservan)

"""


def normalizar_email(valor: str | None) -> str | None:
    """RN01 — Los emails se almacenan en minúsculas"""
    if valor is None:
        return None
    return valor.strip().lower()


def normalizar_texto(valor: str | None) -> str | None:
    """RN02 — Los textos no deben contener espacios al inicio ni al final"""
    if valor is None:
        return None
    return valor.strip()


def normalizar_nombre_usuario(valor: str | None) -> str | None:
    """
    RN03 — Los nombres de usuario se conservan tal cual,
    solo se les quitan los espacios de los bordes.
    """
    if valor is None:
        return None
    return valor.strip()

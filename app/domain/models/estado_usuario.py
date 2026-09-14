from dataclasses import dataclass, field


@dataclass
class EstadoUsuario:
    """
    Estado del usuario autenticado que la autorización necesita conocer.

    Patrón híbrido: este estado se cachea por un TTL corto para no
    consultar la BD en cada request, y se invalida cuando cambia
    (baja, asignación/remoción de rol) para revocar en caliente.
    """

    usuario_id: int
    email: str
    nombre_usuario: str
    activo: bool
    roles: list[str] = field(default_factory=list)

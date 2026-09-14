from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Usuario:
    # Datos obligatorios
    nombre_usuario: str
    email: str
    password_hash: str

    # Datos opcionales
    nombre_completo: str | None = None
    activo: bool = True

    # Marcas temporales — las maneja el sistema
    fecha_creacion: datetime | None = None
    fecha_actualizacion: datetime | None = None

    # Clave primaria — la asigna la BD
    id: int | None = field(default=None)

    # Relaciones — IDs de roles
    ids_roles: list[int] = field(default_factory=list)

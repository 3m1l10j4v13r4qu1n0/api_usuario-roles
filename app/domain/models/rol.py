from dataclasses import dataclass, field


@dataclass
class Rol:
    # Datos obligatorios
    nombre: str

    # Datos opcionales
    descripcion: str | None = None

    # Clave primaria — la asigna la BD
    id: int | None = field(default=None)

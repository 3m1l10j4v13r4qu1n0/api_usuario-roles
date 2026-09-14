from app.domain.exceptions import DatoInvalidoError
from app.domain.models.rol import Rol
from app.domain.ports.rol.rol_command_port import RolCommandPort
from app.domain.services.normalizacion import normalizar_texto

"""
UC7 — Crear rol
"""


class CrearRolUseCase:
    """
    UC7 — Crea un rol nuevo.

    Attributes:
        _repo : RolCommandPort
    """

    def __init__(self, repo: RolCommandPort) -> None:
        self._repo = repo

    async def execute(self, datos: dict):
        """
        Raises:
            DatoInvalidoError — Si el nombre es vacío o el rol ya existe.
        """
        nombre = normalizar_texto(datos.get("nombre"))
        if not nombre:
            raise DatoInvalidoError("El nombre del rol es obligatorio")

        existente = await self._repo.buscar_por_nombre(nombre)
        if existente is not None:
            raise DatoInvalidoError(f"El rol '{nombre}' ya existe")

        rol = Rol(
            nombre=nombre,
            descripcion=normalizar_texto(datos.get("descripcion")),
        )

        return await self._repo.crear(rol)

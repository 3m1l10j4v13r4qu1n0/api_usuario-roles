from app.domain.ports.rol.rol_query_port import RolQueryPort

"""
UC8 — Listar roles
"""


class ListarRolesUseCase:
    """
    UC8 — Obtiene todos los roles almacenados.

    Attributes:
        _repo : RolQueryPort
    """

    def __init__(self, repo: RolQueryPort) -> None:
        self._repo = repo

    async def execute(self) -> list:
        return await self._repo.listar()

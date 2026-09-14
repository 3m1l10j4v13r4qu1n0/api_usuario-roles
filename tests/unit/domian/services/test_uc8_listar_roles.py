"""
Tests del UC8 — Listar roles
Ubicación: tests/unit/domian/services/test_uc8_listar_roles.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

from app.application.use_cases.uc8_listar_roles import ListarRolesUseCase
from app.domain.models.rol import Rol


class FakeRolQueryRepo:
    def __init__(self, roles: list[Rol]):
        self._roles = roles

    async def listar(self):
        return list(self._roles)

    async def obtener_nombres_por_ids(self, ids_roles: list[int]) -> list[str]:
        return [r.nombre for r in self._roles if r.id is not None and r.id in ids_roles]


def run(coro):
    return asyncio.run(coro)


def _rol(id_: int, nombre: str) -> Rol:
    return Rol(id=id_, nombre=nombre)


class TestListarRoles:

    def test_sin_roles_devuelve_lista_vacia(self):
        uc = ListarRolesUseCase(FakeRolQueryRepo([]))
        assert run(uc.execute()) == []

    def test_con_roles_devuelve_todos(self):
        roles = [_rol(1, "ADMIN"), _rol(2, "USUARIO")]
        uc = ListarRolesUseCase(FakeRolQueryRepo(roles))
        resultado = run(uc.execute())

        assert len(resultado) == 2
        assert resultado[0].nombre == "ADMIN"
        assert resultado[1].nombre == "USUARIO"

    def test_devuelve_instancias_rol(self):
        uc = ListarRolesUseCase(FakeRolQueryRepo([_rol(1, "OPERADOR")]))
        resultado = run(uc.execute())

        assert isinstance(resultado[0], Rol)
        assert resultado[0].id == 1

"""
Tests del UC7 — Crear rol
Ubicación: tests/unit/domian/services/test_uc7_crear_rol.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc7_crear_rol import CrearRolUseCase
from app.domain.exceptions import DatoInvalidoError
from app.domain.models.rol import Rol


class FakeRolCommandRepo:
    def __init__(self, roles: list[Rol] | None = None):
        self._roles = list(roles or [])
        self._next_id = 1

    async def buscar_por_nombre(self, nombre: str):
        for r in self._roles:
            if r.nombre == nombre:
                return r
        return None

    async def buscar_por_id(self, rol_id: int):
        for r in self._roles:
            if r.id == rol_id:
                return r
        return None

    async def crear(self, rol: Rol):
        rol.id = self._next_id
        self._next_id += 1
        self._roles.append(rol)
        return rol


def run(coro):
    return asyncio.run(coro)


@pytest.fixture
def crear_rol_uc():
    return CrearRolUseCase(FakeRolCommandRepo())


@pytest.fixture
def crear_rol_uc_con_existente():
    repo = FakeRolCommandRepo([Rol(id=1, nombre="ADMIN", descripcion="Administrador")])
    return CrearRolUseCase(repo)


class TestCrearRol:

    def test_crea_rol_con_descripcion(self, crear_rol_uc):
        rol = run(
            crear_rol_uc.execute({"nombre": "GERENTE", "descripcion": "Gerencia"})
        )

        assert rol.id is not None
        assert rol.nombre == "GERENTE"
        assert rol.descripcion == "Gerencia"

    def test_crea_rol_sin_descripcion(self, crear_rol_uc):
        rol = run(crear_rol_uc.execute({"nombre": "GERENTE"}))

        assert rol.nombre == "GERENTE"
        assert rol.descripcion is None

    def test_normaliza_nombre_y_descripcion(self, crear_rol_uc):
        rol = run(
            crear_rol_uc.execute(
                {"nombre": "  GERENTE  ", "descripcion": "  Gerencia  "}
            )
        )
        assert rol.nombre == "GERENTE"
        assert rol.descripcion == "Gerencia"

    def test_nombre_vacio_lanza(self, crear_rol_uc):
        with pytest.raises(DatoInvalidoError):
            run(crear_rol_uc.execute({"nombre": "   "}))

    def test_nombre_faltante_lanza(self, crear_rol_uc):
        with pytest.raises(DatoInvalidoError):
            run(crear_rol_uc.execute({}))

    def test_nombre_duplicado_lanza(self, crear_rol_uc_con_existente):
        with pytest.raises(DatoInvalidoError):
            run(crear_rol_uc_con_existente.execute({"nombre": "ADMIN"}))

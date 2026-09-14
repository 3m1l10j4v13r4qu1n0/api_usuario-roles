"""
Tests del UC9 — Asignar rol a usuario
Ubicación: tests/unit/domian/services/test_uc9_asignar_rol.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc9_asignar_rol import AsignarRolUseCase
from app.domain.exceptions import RolNoEncontradoError, UsuarioNoEncontradoError
from app.domain.models.rol import Rol
from app.domain.models.usuario import Usuario


class FakeUsuarioCommandRepo:
    def __init__(self, usuarios: list[Usuario]):
        self._usuarios = {u.id: u for u in usuarios}

    async def asignar_rol(self, usuario_id: int, rol_id: int):
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            return None
        if rol_id not in usuario.ids_roles:
            usuario.ids_roles = list(usuario.ids_roles) + [rol_id]
        return usuario


class FakeRolCommandRepo:
    def __init__(self, roles: list[Rol]):
        self._roles = {r.id: r for r in roles}

    async def buscar_por_id(self, rol_id: int):
        return self._roles.get(rol_id)


def run(coro):
    return asyncio.run(coro)


def usuario_sin_roles() -> Usuario:
    return Usuario(
        id=99,
        nombre_usuario="juan_perez",
        email="juan@test.com",
        password_hash="fake:clave1234",
    )


ROL_ADMIN = Rol(id=1, nombre="ADMIN", descripcion="Administrador")


@pytest.fixture
def asignar_rol_uc():
    repo_usuarios = FakeUsuarioCommandRepo([usuario_sin_roles()])
    repo_roles = FakeRolCommandRepo([ROL_ADMIN])
    return AsignarRolUseCase(repo_usuarios, repo_roles)


class TestAsignarRol:

    def test_asignacion_exitosa_agrega_rol_al_usuario(self, asignar_rol_uc):
        usuario = run(asignar_rol_uc.execute(99, 1))

        assert usuario.id == 99
        assert 1 in usuario.ids_roles

    def test_rol_inexistente_lanza(self):
        repo_usuarios = FakeUsuarioCommandRepo([usuario_sin_roles()])
        repo_roles = FakeRolCommandRepo([])
        uc = AsignarRolUseCase(repo_usuarios, repo_roles)

        with pytest.raises(RolNoEncontradoError):
            run(uc.execute(99, 123))

    def test_usuario_inexistente_lanza(self):
        repo_usuarios = FakeUsuarioCommandRepo([])
        repo_roles = FakeRolCommandRepo([ROL_ADMIN])
        uc = AsignarRolUseCase(repo_usuarios, repo_roles)

        with pytest.raises(UsuarioNoEncontradoError):
            run(uc.execute(999, 1))

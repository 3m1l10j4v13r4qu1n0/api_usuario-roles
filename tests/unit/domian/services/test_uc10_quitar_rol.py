"""
Tests del UC10 — Quitar rol a usuario
Ubicación: tests/unit/domian/services/test_uc10_quitar_rol.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc10_quitar_rol import QuitarRolUseCase
from app.domain.exceptions import RolNoEncontradoError, UsuarioNoEncontradoError
from app.domain.models.rol import Rol
from app.domain.models.usuario import Usuario


class FakeUsuarioCommandRepo:
    def __init__(self, usuarios: list[Usuario]):
        self._usuarios = {u.id: u for u in usuarios}

    async def quitar_rol(self, usuario_id: int, rol_id: int):
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            return None
        usuario.ids_roles = [r for r in usuario.ids_roles if r != rol_id]
        return usuario


class FakeRolCommandRepo:
    def __init__(self, roles: list[Rol]):
        self._roles = {r.id: r for r in roles}

    async def buscar_por_id(self, rol_id: int):
        return self._roles.get(rol_id)


class FakeEstadoCache:
    def __init__(self):
        self.invalidados: list[int] = []

    async def obtener(self, usuario_id: int):
        return None

    async def guardar(self, estado) -> None:
        pass

    async def invalidar(self, usuario_id: int) -> None:
        self.invalidados.append(usuario_id)


def run(coro):
    return asyncio.run(coro)


def usuario_con_admin() -> Usuario:
    return Usuario(
        id=99,
        nombre_usuario="juan_perez",
        email="juan@test.com",
        password_hash="fake:clave1234",
        ids_roles=[1, 2],
    )


ROL_ADMIN = Rol(id=1, nombre="ADMIN", descripcion="Administrador")


@pytest.fixture
def quitar_rol_uc():
    repo_usuarios = FakeUsuarioCommandRepo([usuario_con_admin()])
    repo_roles = FakeRolCommandRepo([ROL_ADMIN])
    cache = FakeEstadoCache()
    return QuitarRolUseCase(repo_usuarios, repo_roles, cache)


class TestQuitarRol:

    def test_quitar_rol_remueve_el_rol_del_usuario(self, quitar_rol_uc):
        usuario = run(quitar_rol_uc.execute(99, 1))

        assert usuario.id == 99
        assert 1 not in usuario.ids_roles
        assert 2 in usuario.ids_roles

    def test_quitar_rol_invalida_estado_en_cache(self, quitar_rol_uc):
        run(quitar_rol_uc.execute(99, 1))

        assert quitar_rol_uc._estado_cache.invalidados == [99]

    def test_rol_inexistente_lanza(self):
        repo_usuarios = FakeUsuarioCommandRepo([usuario_con_admin()])
        repo_roles = FakeRolCommandRepo([])
        uc = QuitarRolUseCase(repo_usuarios, repo_roles, FakeEstadoCache())

        with pytest.raises(RolNoEncontradoError):
            run(uc.execute(99, 123))

    def test_usuario_inexistente_lanza(self):
        repo_usuarios = FakeUsuarioCommandRepo([])
        repo_roles = FakeRolCommandRepo([ROL_ADMIN])
        uc = QuitarRolUseCase(repo_usuarios, repo_roles, FakeEstadoCache())

        with pytest.raises(UsuarioNoEncontradoError):
            run(uc.execute(999, 1))

"""
Tests del UC6 — Dar de baja usuario
Ubicación: tests/unit/domian/services/test_uc6_dar_de_baja_usuario.py

Baja lógica: no se borra físicamente, solo se marca activo = False.
Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc6_dar_de_baja_usuario import DarDeBajaUsuarioUseCase
from app.domain.exceptions import UsuarioNoEncontradoError
from app.domain.models.usuario import Usuario


class FakeUsuarioCommandRepo:
    def __init__(self, usuarios: list[Usuario]):
        self._usuarios = {u.id: u for u in usuarios}

    async def dar_de_baja(self, usuario_id: int):
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            return None
        usuario.activo = False
        return usuario


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


def usuario_activo() -> Usuario:
    return Usuario(
        id=99,
        nombre_usuario="juan_perez",
        email="juan@test.com",
        password_hash="fake:clave1234",
        activo=True,
    )


class TestDarDeBajaUsuario:

    def test_baja_logica_marca_inactivo(self):
        uc = DarDeBajaUsuarioUseCase(
            FakeUsuarioCommandRepo([usuario_activo()]), FakeEstadoCache()
        )
        usuario = run(uc.execute(99))

        assert usuario.activo is False

    def test_baja_invalida_estado_en_cache(self):
        cache = FakeEstadoCache()
        uc = DarDeBajaUsuarioUseCase(FakeUsuarioCommandRepo([usuario_activo()]), cache)
        run(uc.execute(99))

        assert cache.invalidados == [99]

    def test_usuario_inexistente_lanza(self):
        uc = DarDeBajaUsuarioUseCase(FakeUsuarioCommandRepo([]), FakeEstadoCache())
        with pytest.raises(UsuarioNoEncontradoError):
            run(uc.execute(99))

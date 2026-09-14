"""
Tests del UC4 — Obtener usuario por ID
Ubicación: tests/unit/domian/services/test_uc4_obtener_usuario_por_id.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc4_obtener_usuario_por_id import (
    ObtenerUsuarioPorIdUseCase,
)
from app.domain.exceptions import UsuarioNoEncontradoError
from app.domain.models.usuario import Usuario


class FakeUsuarioQueryRepo:
    def __init__(self, usuarios: list[Usuario]):
        self._usuarios = usuarios

    async def listar(self):
        return list(self._usuarios)

    async def obtener_por_id(self, usuario_id: int):
        for u in self._usuarios:
            if u.id == usuario_id:
                return u
        return None

    async def obtener_por_email(self, email: str):
        for u in self._usuarios:
            if u.email == email:
                return u
        return None


def run(coro):
    return asyncio.run(coro)


USUARIO = Usuario(
    id=99,
    nombre_usuario="juan_perez",
    email="juan@test.com",
    password_hash="fake:clave1234",
)


class TestObtenerUsuarioPorId:

    def test_usuario_existente_se_devuelve(self):
        uc = ObtenerUsuarioPorIdUseCase(FakeUsuarioQueryRepo([USUARIO]))
        usuario = run(uc.execute(99))

        assert usuario.id == 99
        assert usuario.email == "juan@test.com"

    def test_usuario_inexistente_lanza(self):
        uc = ObtenerUsuarioPorIdUseCase(FakeUsuarioQueryRepo([USUARIO]))
        with pytest.raises(UsuarioNoEncontradoError):
            run(uc.execute(123))

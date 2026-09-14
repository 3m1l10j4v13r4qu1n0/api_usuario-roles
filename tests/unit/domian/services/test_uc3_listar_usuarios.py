"""
Tests del UC3 — Listar usuarios
Ubicación: tests/unit/domian/services/test_uc3_listar_usuarios.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

from app.application.use_cases.uc3_listar_usuarios import ListarUsuariosUseCase
from app.domain.models.usuario import Usuario
from app.domain.ports.usuario.usuario_query_port import UsuarioQueryPort


class FakeUsuarioQueryRepo(UsuarioQueryPort):
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


def _usuario(id_: int, nombre: str, email: str) -> Usuario:
    return Usuario(
        id=id_,
        nombre_usuario=nombre,
        email=email,
        password_hash="fake:clave1234",
    )


class TestListarUsuarios:

    def test_sin_usuarios_devuelve_lista_vacia(self):
        uc = ListarUsuariosUseCase(FakeUsuarioQueryRepo([]))
        assert run(uc.execute()) == []

    def test_con_usuarios_devuelve_todos(self):
        usuarios = [
            _usuario(1, "admin", "admin@test.com"),
            _usuario(2, "juan_perez", "juan@test.com"),
        ]
        uc = ListarUsuariosUseCase(FakeUsuarioQueryRepo(usuarios))
        resultado = run(uc.execute())

        assert len(resultado) == 2
        assert resultado[0].nombre_usuario == "admin"
        assert resultado[1].email == "juan@test.com"

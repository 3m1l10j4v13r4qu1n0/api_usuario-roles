"""
Tests del UC5 — Actualizar usuario
Ubicación: tests/unit/domian/services/test_uc5_actualizar_usuario.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc5_actualizar_usuario import ActualizarUsuarioUseCase
from app.domain.exceptions import EmailDuplicadoError, UsuarioNoEncontradoError
from app.domain.models.usuario import Usuario


class FakeUsuarioCommandRepo:
    def __init__(self, usuarios: list[Usuario]):
        self._usuarios = {u.id: u for u in usuarios}

    async def buscar_por_email(self, email: str):
        for u in self._usuarios.values():
            if u.email == email:
                return u
        return None

    async def buscar_por_email_excluyendo_id(self, email: str, usuario_id: int):
        for u in self._usuarios.values():
            if u.email == email and u.id != usuario_id:
                return u
        return None

    async def crear(self, usuario: Usuario):
        return usuario

    async def actualizar(self, usuario_id: int, campos: dict):
        usuario = self._usuarios.get(usuario_id)
        if usuario is None:
            return None
        for campo, valor in campos.items():
            setattr(usuario, campo, valor)
        return usuario

    async def dar_de_baja(self, usuario_id: int):
        return None

    async def asignar_rol(self, usuario_id: int, rol_id: int):
        return None


class FakeHasher:
    def hash_password(self, password: str) -> str:
        return f"fake:{password}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        return f"fake:{password}" == password_hash


class StubUpdate:
    """Simula un schema Pydantic sin depender del framework."""

    def __init__(self, **campos):
        self._campos = campos

    def model_dump(self, exclude_unset=True):
        return dict(self._campos)


def run(coro):
    return asyncio.run(coro)


def usuario_base() -> Usuario:
    return Usuario(
        id=99,
        nombre_usuario="juan_perez",
        email="juan@test.com",
        password_hash="fake:clave1234",
        nombre_completo="Juan Pérez",
    )


@pytest.fixture
def actualizar_uc():
    repo = FakeUsuarioCommandRepo([usuario_base()])
    return ActualizarUsuarioUseCase(repo, FakeHasher())


@pytest.fixture
def actualizar_uc_con_email_en_uso():
    repo = FakeUsuarioCommandRepo(
        [
            usuario_base(),
            Usuario(
                id=100,
                nombre_usuario="otro",
                email="otro@test.com",
                password_hash="fake:clave1234",
            ),
        ]
    )
    return ActualizarUsuarioUseCase(repo, FakeHasher())


class TestActualizarUsuario:

    def test_actualiza_nombre_usuario_y_nombre_completo(self, actualizar_uc):
        usuario = run(
            actualizar_uc.execute(
                99, StubUpdate(nombre_usuario="nuevo_nombre", nombre_completo="Nuevo")
            )
        )
        assert usuario.nombre_usuario == "nuevo_nombre"
        assert usuario.nombre_completo == "Nuevo"
        assert usuario.email == "juan@test.com"

    def test_actualiza_email_normalizado(self, actualizar_uc):
        usuario = run(actualizar_uc.execute(99, StubUpdate(email="Juan@Nuevo.COM")))
        assert usuario.email == "juan@nuevo.com"

    def test_cambia_password_y_hashea(self, actualizar_uc):
        usuario = run(actualizar_uc.execute(99, StubUpdate(password="nueva1234")))
        assert usuario.password_hash == "fake:nueva1234"

    def test_email_en_uso_por_otro_lanza(self, actualizar_uc_con_email_en_uso):
        with pytest.raises(EmailDuplicadoError):
            run(
                actualizar_uc_con_email_en_uso.execute(
                    99, StubUpdate(email="otro@test.com")
                )
            )

    def test_mismo_email_no_lanza(self, actualizar_uc):
        usuario = run(actualizar_uc.execute(99, StubUpdate(email="juan@test.com")))
        assert usuario.email == "juan@test.com"

    def test_usuario_inexistente_lanza(self, actualizar_uc):
        with pytest.raises(UsuarioNoEncontradoError):
            run(actualizar_uc.execute(999, StubUpdate(nombre_usuario="x")))

    def test_sin_campos_no_rompe(self, actualizar_uc):
        usuario = run(actualizar_uc.execute(99, StubUpdate()))
        assert usuario.id == 99
        assert usuario.nombre_usuario == "juan_perez"

"""
Tests del UC2 — Registrar usuario
Ubicación: tests/unit/domian/services/test_uc2_registrar_usuario.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc2_registrar_usuario import RegistrarUsuarioUseCase
from app.domain.exceptions import DatoInvalidoError, EmailDuplicadoError
from app.domain.models.rol import Rol
from app.domain.models.usuario import Usuario


class FakeUsuarioCommandRepo:
    def __init__(self, usuarios_por_email: dict[str, Usuario] | None = None):
        self._usuarios = dict(usuarios_por_email or {})
        self._next_id = 1

    async def buscar_por_email(self, email: str):
        return self._usuarios.get(email)

    async def crear(self, usuario: Usuario):
        usuario.id = self._next_id
        self._next_id += 1
        self._usuarios[usuario.email] = usuario
        return usuario


class FakeRolCommandRepo:
    def __init__(self, roles_por_nombre: dict[str, Rol] | None = None):
        self._roles = dict(roles_por_nombre or {})

    async def buscar_por_nombre(self, nombre: str):
        return self._roles.get(nombre)


class FakeHasher:
    def hash_password(self, password: str) -> str:
        return f"fake:{password}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        return f"fake:{password}" == password_hash


def _roles_sin_rol_defecto() -> FakeRolCommandRepo:
    return FakeRolCommandRepo()


def _roles_con_rol_defecto() -> FakeRolCommandRepo:
    return FakeRolCommandRepo({"USUARIO": Rol(id=2, nombre="USUARIO")})


@pytest.fixture
def registrar_uc():
    repo = FakeUsuarioCommandRepo()
    rol_repo = _roles_con_rol_defecto()
    return RegistrarUsuarioUseCase(repo, rol_repo, FakeHasher())


@pytest.fixture
def registrar_uc_sin_rol_defecto():
    repo = FakeUsuarioCommandRepo()
    rol_repo = _roles_sin_rol_defecto()
    return RegistrarUsuarioUseCase(repo, rol_repo, FakeHasher())


@pytest.fixture
def registrar_uc_con_email_existente():
    repo = FakeUsuarioCommandRepo(
        {
            "juan@test.com": Usuario(
                nombre_usuario="juan_perez",
                email="juan@test.com",
                password_hash="fake:clave1234",
            )
        }
    )
    rol_repo = _roles_con_rol_defecto()
    return RegistrarUsuarioUseCase(repo, rol_repo, FakeHasher())


def run(coro):
    return asyncio.run(coro)


DATOS_VALIDOS = {
    "nombre_usuario": "juan_perez",
    "email": "Juan@Test.COM",
    "password": "clave1234",
    "nombre_completo": "Juan Pérez",
}


class TestRegistrarUsuario:

    def test_registro_exitoso_devuelve_usuario(self, registrar_uc):
        usuario = run(registrar_uc.execute(DATOS_VALIDOS))

        assert usuario.id is not None
        assert usuario.email == "juan@test.com"
        assert usuario.password_hash == "fake:clave1234"
        assert usuario.nombre_completo == "Juan Pérez"
        assert usuario.activo is True
        assert usuario.ids_roles == [2]

    def test_registro_autoasigna_rol_usuario_por_defecto(self, registrar_uc):
        usuario = run(registrar_uc.execute(DATOS_VALIDOS))
        assert 2 in usuario.ids_roles

    def test_registro_sin_rol_defecto_crea_sin_roles(
        self, registrar_uc_sin_rol_defecto
    ):
        usuario = run(registrar_uc_sin_rol_defecto.execute(DATOS_VALIDOS))
        assert usuario.ids_roles == []

    def test_registro_normaliza_email_y_nombre(self, registrar_uc):
        datos = {
            **DATOS_VALIDOS,
            "email": "  Juan@Test.COM  ",
            "nombre_usuario": "  juan_perez  ",
        }
        usuario = run(registrar_uc.execute(datos))
        assert usuario.email == "juan@test.com"
        assert usuario.nombre_usuario == "juan_perez"

    def test_registro_sin_nombre_completo(self, registrar_uc):
        datos = {k: v for k, v in DATOS_VALIDOS.items() if k != "nombre_completo"}
        usuario = run(registrar_uc.execute(datos))
        assert usuario.nombre_completo is None

    def test_email_duplicado_lanza(self, registrar_uc_con_email_existente):
        with pytest.raises(EmailDuplicadoError):
            run(registrar_uc_con_email_existente.execute(DATOS_VALIDOS))

    def test_email_duplicado_normaliza_mayusculas(
        self, registrar_uc_con_email_existente
    ):
        datos = {**DATOS_VALIDOS, "email": "JUAN@TEST.COM"}
        with pytest.raises(EmailDuplicadoError):
            run(registrar_uc_con_email_existente.execute(datos))

    def test_email_invalido_lanza(self, registrar_uc):
        datos = {**DATOS_VALIDOS, "email": "juan@@test.com"}
        with pytest.raises(DatoInvalidoError):
            run(registrar_uc.execute(datos))

    def test_password_corta_lanza(self, registrar_uc):
        datos = {**DATOS_VALIDOS, "password": "1234567"}
        with pytest.raises(DatoInvalidoError):
            run(registrar_uc.execute(datos))

    def test_nombre_usuario_vacio_lanza(self, registrar_uc):
        datos = {**DATOS_VALIDOS, "nombre_usuario": "  "}
        with pytest.raises(DatoInvalidoError):
            run(registrar_uc.execute(datos))

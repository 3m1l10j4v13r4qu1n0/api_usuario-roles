"""
Tests de auth_service.py
Ubicación: tests/unidad/domian/services/test_auth_service.py

Usa un FakePasswordHasher (en memoria) para aislar el dominio.
"""

import pytest

from app.domain.exceptions import CredencialesInvalidasError, NoAutorizadoError
from app.domain.models.usuario import Usuario
from app.domain.ports.authentication.password_hasher_port import PasswordHasherPort
from app.domain.services.auth_service import (
    autorizar,
    verificar_credenciales,
)


class FakePasswordHasher(PasswordHasherPort):
    """Hasher en memoria para tests: el "hash" es el texto con prefijo `fake:`."""

    def hash_password(self, password: str) -> str:
        return f"fake:{password}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        return f"fake:{password}" == password_hash


@pytest.fixture
def hasher():
    return FakePasswordHasher()


@pytest.fixture
def usuario_activo():
    return Usuario(
        id=1,
        nombre_usuario="juan",
        email="juan@test.com",
        password_hash="fake:clave1234",
        activo=True,
    )


@pytest.fixture
def usuario_inactivo():
    return Usuario(
        id=2,
        nombre_usuario="ana",
        email="ana@test.com",
        password_hash="fake:clave1234",
        activo=False,
    )


class TestVerificarCredenciales:

    def test_credenciales_validas_devuelve_usuario(self, usuario_activo, hasher):
        resultado = verificar_credenciales(usuario_activo, "clave1234", hasher)
        assert resultado is usuario_activo

    def test_password_incorrecto_lanza(self, usuario_activo, hasher):
        with pytest.raises(CredencialesInvalidasError):
            verificar_credenciales(usuario_activo, "clave0000", hasher)

    def test_usuario_inexistente_lanza(self, hasher):
        with pytest.raises(CredencialesInvalidasError):
            verificar_credenciales(None, "clave1234", hasher)

    def test_usuario_inactivo_lanza(self, usuario_inactivo, hasher):
        with pytest.raises(CredencialesInvalidasError):
            verificar_credenciales(usuario_inactivo, "clave1234", hasher)


class TestAutorizar:

    def test_usuario_con_rol_requerido_ok(self):
        autorizar(["ADMIN"], ["ADMIN"])

    def test_usuario_sin_rol_requerido_lanza(self):
        with pytest.raises(NoAutorizadoError):
            autorizar(["USUARIO"], ["ADMIN"])

    def test_sin_roles_requeridos_permite(self):
        autorizar([], [])

    def test_roles_sin_permisos_vacios_lanza(self):
        with pytest.raises(NoAutorizadoError):
            autorizar([], ["ADMIN"])

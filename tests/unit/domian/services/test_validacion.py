"""
Tests de validacion.py
Ubicación: tests/unit/domian/services/test_validacion.py

Cubre:
    - validar_email()
    - validar_nombre_usuario()
    - validar_password()
"""

import pytest

from app.domain.exceptions import DatoInvalidoError
from app.domain.services.validacion import (
    normalizar_y_validar_email,
    validar_email,
    validar_nombre_usuario,
    validar_password,
)


class TestValidarEmail:

    def test_email_valido_no_lanza(self):
        validar_email("juan@test.com")

    def test_email_invalido_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_email("juan@@test.com")

    def test_email_vacio_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_email("  ")

    def test_none_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_email(None)

    def test_normalizar_y_validar_devuelve_email_en_minusculas(self):
        assert normalizar_y_validar_email("  Juan@Test.COM  ") == "juan@test.com"


class TestValidarNombreUsuario:

    def test_nombre_valido_no_lanza(self):
        validar_nombre_usuario("juan_perez")

    def test_nombre_vacio_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_nombre_usuario("  ")

    def test_none_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_nombre_usuario(None)


class TestValidarPassword:

    def test_password_valida_no_lanza(self):
        validar_password("clave1234")

    def test_password_corta_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_password("1234567")

    def test_password_vacia_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_password("")

    def test_none_lanza(self):
        with pytest.raises(DatoInvalidoError):
            validar_password(None)

"""
Tests de normalizacion.py
Ubicación: tests/unit/domian/services/test_normalizacion.py

Cubre:
    - normalizar_email()
    - normalizar_texto()
    - normalizar_nombre_usuario()
"""

from app.domain.services.normalizacion import (
    normalizar_email,
    normalizar_nombre_usuario,
    normalizar_texto,
)


class TestNormalizarEmail:

    def test_convierte_a_minusculas(self):
        """RN01 — los emails se almacenan en minúsculas."""
        assert normalizar_email("JUAN@TEST.COM") == "juan@test.com"

    def test_elimina_espacios(self):
        assert normalizar_email("  juan@test.com  ") == "juan@test.com"

    def test_minusculas_y_sin_espacios(self):
        assert normalizar_email("  Juan@Test.Com  ") == "juan@test.com"

    def test_none_retorna_none(self):
        assert normalizar_email(None) is None


class TestNormalizarTexto:

    def test_elimina_espacios_inicio(self):
        assert normalizar_texto("  valor") == "valor"

    def test_elimina_espacios_final(self):
        assert normalizar_texto("valor  ") == "valor"

    def test_none_retorna_none(self):
        assert normalizar_texto(None) is None


class TestNormalizarNombreUsuario:

    def test_conserva_mayusculas(self):
        """RN03 — el nombre de usuario se conserva tal cual."""
        assert normalizar_nombre_usuario("JuanPérez") == "JuanPérez"

    def test_elimina_espacios(self):
        assert normalizar_nombre_usuario("  juan_perez  ") == "juan_perez"

    def test_none_retorna_none(self):
        assert normalizar_nombre_usuario(None) is None

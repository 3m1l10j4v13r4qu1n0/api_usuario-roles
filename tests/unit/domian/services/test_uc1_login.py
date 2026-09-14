"""
Tests del UC1 — Login
Ubicación: tests/unit/domian/services/test_uc1_login.py

Usa fakes (en memoria) para aislar el caso de uso de la infraestructura.
"""

import asyncio

import pytest

from app.application.use_cases.uc1_login import LoginUseCase
from app.domain.exceptions import CredencialesInvalidasError
from app.domain.models.usuario import Usuario


class FakeUsuarioQueryRepo:
    def __init__(self, usuarios: list[Usuario]):
        self._usuarios = {u.email: u for u in usuarios}

    async def listar(self):
        return list(self._usuarios.values())

    async def obtener_por_id(self, usuario_id: int):
        for u in self._usuarios.values():
            if u.id == usuario_id:
                return u
        return None

    async def obtener_por_email(self, email: str):
        return self._usuarios.get(email)


class FakeRolQueryRepo:
    def __init__(self, nombres_por_id: dict[int, str]):
        self._nombres = nombres_por_id

    async def listar(self):
        return []

    async def obtener_nombres_por_ids(self, ids_roles: list[int]) -> list[str]:
        return [self._nombres[i] for i in ids_roles if i in self._nombres]


class FakeHasher:
    def hash_password(self, password: str) -> str:
        return f"fake:{password}"

    def verify_password(self, password: str, password_hash: str) -> bool:
        return f"fake:{password}" == password_hash


class FakeTokenProvider:
    def crear_token(self, usuario_id: int, roles: list[str]) -> str:
        return f"token.{usuario_id}.{','.join(roles)}"

    def decodificar_token(self, token: str) -> dict:
        return {"sub": token.split(".")[1]}


@pytest.fixture
def usuario_admin():
    return Usuario(
        id=1,
        nombre_usuario="admin",
        email="admin@test.com",
        password_hash="fake:clave1234",
        activo=True,
        ids_roles=[1],
    )


@pytest.fixture
def login_uc(usuario_admin):
    usuario_repo = FakeUsuarioQueryRepo([usuario_admin])
    rol_repo = FakeRolQueryRepo({1: "ADMIN"})
    hasher = FakeHasher()
    token_provider = FakeTokenProvider()
    return LoginUseCase(usuario_repo, rol_repo, hasher, token_provider)


def run(coro):
    return asyncio.run(coro)


class TestLogin:

    def test_login_valido_devuelve_token(self, login_uc):
        resultado = run(login_uc.execute("admin@test.com", "clave1234"))
        assert resultado["access_token"] == "token.1.ADMIN"
        assert resultado["token_type"] == "bearer"
        assert resultado["email"] == "admin@test.com"
        assert resultado["roles"] == ["ADMIN"]

    def test_login_ignora_mayusculas_en_email(self, login_uc):
        resultado = run(login_uc.execute("ADMIN@TEST.COM", "clave1234"))
        assert resultado["id"] == 1

    def test_login_password_incorrecto_lanza(self, login_uc):
        with pytest.raises(CredencialesInvalidasError):
            run(login_uc.execute("admin@test.com", "clave0000"))

    def test_login_email_inexistente_lanza(self, login_uc):
        with pytest.raises(CredencialesInvalidasError):
            run(login_uc.execute("no@existe.com", "clave1234"))

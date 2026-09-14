"""
Fase 4 — Tests de integración contra BD real.

Flujo: registrar → login → /auth/me → asignar rol ADMIN → re-login →
listar roles → crear rol → baja lógica → login rechazado.
Incluye flujos de error: password incorrecta (401) y email duplicado (409).

Correr con:  python -m pytest -m integracion
"""

import pytest

pytestmark = pytest.mark.integracion


def _crear_usuario(cliente, email: str, password: str = "clave1234"):
    return cliente.post(
        "/usuarios/",
        json={
            "nombre_usuario": f"u_{email.split('@')[0]}",
            "email": email,
            "password": password,
        },
    )


def _login(cliente, email: str, password: str = "clave1234"):
    return cliente.post(
        "/auth/login",
        json={"email": email, "password": password},
    )


def _headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


class TestFlujoCompleto:

    def test_registrar_login_me_asignar_rol_y_listar_roles(self, cliente):
        resp = _crear_usuario(cliente, "flujo@test.com")
        assert resp.status_code == 201
        usuario_id = resp.json()["id"]

        resp = _login(cliente, "flujo@test.com")
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = _headers(token)

        resp = cliente.get("/auth/me", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "flujo@test.com"

        resp = cliente.post(
            f"/usuarios/{usuario_id}/roles", headers=headers, json={"id_rol": 1}
        )
        assert resp.status_code == 200
        assert 1 in resp.json()["ids_roles"]

        resp = _login(cliente, "flujo@test.com")
        assert resp.status_code == 200
        assert resp.json()["roles"] == ["ADMIN"]
        headers = _headers(resp.json()["access_token"])

        resp = cliente.get("/roles/", headers=headers)
        assert resp.status_code == 200
        nombres = [r["nombre"] for r in resp.json()]
        assert "ADMIN" in nombres and "USUARIO" in nombres

        resp = cliente.post(
            "/roles/", headers=headers, json={"nombre": "OPERADOR", "descripcion": "Op"}
        )
        assert resp.status_code == 201
        assert resp.json()["nombre"] == "OPERADOR"

        resp = cliente.get("/roles/", headers=headers)
        assert resp.status_code == 200
        assert "OPERADOR" in [r["nombre"] for r in resp.json()]

    def test_baja_logica_rechaza_login(self, cliente):
        resp = _crear_usuario(cliente, "baja@test.com")
        assert resp.status_code == 201
        usuario_id = resp.json()["id"]

        token = _login(cliente, "baja@test.com").json()["access_token"]
        resp = cliente.delete(f"/usuarios/{usuario_id}", headers=_headers(token))
        assert resp.status_code == 200
        assert resp.json()["activo"] is False

        resp = _login(cliente, "baja@test.com")
        assert resp.status_code == 401

    def test_login_password_incorrecto_devuelve_401(self, cliente):
        _crear_usuario(cliente, "err@test.com")
        resp = cliente.post(
            "/auth/login", json={"email": "err@test.com", "password": "clave0000"}
        )
        assert resp.status_code == 401

    def test_email_duplicado_devuelve_409(self, cliente):
        assert _crear_usuario(cliente, "dup@test.com").status_code == 201
        resp = _crear_usuario(cliente, "dup@test.com", password="otraclave")
        assert resp.status_code == 409
        assert "ya está registrado" in resp.json()["error"]

    def test_endpoints_protegidos_sin_token_devuelven_401(self, cliente):
        resp = cliente.get("/usuarios/")
        assert resp.status_code == 401

"""
Fase 4 — Tests de integración contra BD real.

Flujo: registrar → login → /auth/me → asignar rol ADMIN → listar roles →
crear rol → baja lógica → login rechazado.
Incluye flujos de error: password incorrecta (401) y email duplicado (409).

Fase 5 — El registro autoasigna USUARIO y la asignación/remoción de roles
exige rol ADMIN (se usa el bootstrap `token_admin`). La autorización lee
el estado real del usuario (patrón híbrido), no las claims del JWT.

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

    def test_registrar_login_me_asignar_rol_y_listar_roles(self, cliente, token_admin):
        resp = _crear_usuario(cliente, "flujo@test.com")
        assert resp.status_code == 201
        usuario_id = resp.json()["id"]
        assert 2 in resp.json()["ids_roles"]  # rol USUARIO autoasignado

        resp = _login(cliente, "flujo@test.com")
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = _headers(token)

        resp = cliente.get("/auth/me", headers=headers)
        assert resp.status_code == 200
        assert resp.json()["email"] == "flujo@test.com"
        assert "USUARIO" in resp.json()["roles"]

        # Asignar rol exige ADMIN: el token del propio usuario no alcanza
        resp = cliente.post(
            f"/usuarios/{usuario_id}/roles", headers=headers, json={"id_rol": 1}
        )
        assert resp.status_code == 403

        resp = cliente.post(
            f"/usuarios/{usuario_id}/roles",
            headers=_headers(token_admin),
            json={"id_rol": 1},
        )
        assert resp.status_code == 200
        assert 1 in resp.json()["ids_roles"]

        # Sin re-login: la revocación en caliente (cache invalidado) hace que
        # el token viejo ya vea ADMIN al autorizar
        resp = cliente.get("/roles/", headers=headers)
        assert resp.status_code == 200
        nombres = [r["nombre"] for r in resp.json()]
        assert "ADMIN" in nombres and "USUARIO" in nombres

        resp = _login(cliente, "flujo@test.com")
        assert resp.status_code == 200
        assert "ADMIN" in resp.json()["roles"]
        headers_admin = _headers(resp.json()["access_token"])

        resp = cliente.post(
            "/roles/",
            headers=headers_admin,
            json={"nombre": "OPERADOR", "descripcion": "Op"},
        )
        assert resp.status_code == 201
        assert resp.json()["nombre"] == "OPERADOR"

        resp = cliente.get("/roles/", headers=headers_admin)
        assert resp.status_code == 200
        assert "OPERADOR" in [r["nombre"] for r in resp.json()]

    def test_baja_logica_rechaza_login(self, cliente, token_admin):
        resp = _crear_usuario(cliente, "baja@test.com")
        assert resp.status_code == 201
        usuario_id = resp.json()["id"]

        resp = cliente.delete(f"/usuarios/{usuario_id}", headers=_headers(token_admin))
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

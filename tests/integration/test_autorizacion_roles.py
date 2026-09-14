"""
Fase 5 — Tests de integración de autorización por rol (patrón híbrido).

Cubren: política de roles por endpoint (403), ownership (ADMIN o el propio
usuario), revocación en caliente (asignar/quitar rol sin re-login) y denegación
de usuarios inactivos con token vigente.

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


class TestAutorizacionPorRol:

    def test_registro_autoasigna_rol_usuario(self, cliente):
        resp = _crear_usuario(cliente, "auto@test.com")
        assert resp.status_code == 201
        assert resp.json()["ids_roles"] == [2]

    def test_403_sin_rol_admin_en_endpoints_admin(self, cliente):
        _crear_usuario(cliente, "normal@test.com")
        token = _login(cliente, "normal@test.com").json()["access_token"]
        headers = _headers(token)

        resp = cliente.get("/usuarios/", headers=headers)
        assert resp.status_code == 403

        resp = cliente.get("/roles/", headers=headers)
        assert resp.status_code == 403

        resp = cliente.post("/roles/", headers=headers, json={"nombre": "NORMAL"})
        assert resp.status_code == 403

    def test_mismo_usuario_puede_ver_y_editar_su_perfil(self, cliente):
        resp_a = _crear_usuario(cliente, "dueno@test.com")
        id_a = resp_a.json()["id"]

        token_a = _login(cliente, "dueno@test.com").json()["access_token"]

        resp = cliente.get(f"/usuarios/{id_a}", headers=_headers(token_a))
        assert resp.status_code == 200
        assert resp.json()["id"] == id_a

        resp = cliente.patch(
            f"/usuarios/{id_a}",
            headers=_headers(token_a),
            json={"nombre_completo": "Dueno Editado"},
        )
        assert resp.status_code == 200
        assert resp.json()["nombre_completo"] == "Dueno Editado"

    def test_otro_usuario_no_admin_obtiene_403(self, cliente):
        resp_a = _crear_usuario(cliente, "dueno2@test.com")
        _crear_usuario(cliente, "otro2@test.com")
        id_a = resp_a.json()["id"]

        token_b = _login(cliente, "otro2@test.com").json()["access_token"]
        headers_b = _headers(token_b)

        resp = cliente.get(f"/usuarios/{id_a}", headers=headers_b)
        assert resp.status_code == 403

        resp = cliente.patch(
            f"/usuarios/{id_a}", headers=headers_b, json={"nombre_completo": "Hack"}
        )
        assert resp.status_code == 403

    def test_admin_puede_operar_sobre_cualquier_usuario(self, cliente, token_admin):
        resp = _crear_usuario(cliente, "adminop@test.com")
        usuario_id = resp.json()["id"]
        headers_admin = _headers(token_admin)

        resp = cliente.get(f"/usuarios/{usuario_id}", headers=headers_admin)
        assert resp.status_code == 200

        resp = cliente.patch(
            f"/usuarios/{usuario_id}",
            headers=headers_admin,
            json={"nombre_completo": "Editado por admin"},
        )
        assert resp.status_code == 200

        resp = cliente.delete(f"/usuarios/{usuario_id}", headers=headers_admin)
        assert resp.status_code == 200
        assert resp.json()["activo"] is False


class TestRevocacionEnCaliente:

    def test_asignar_rol_se_refleja_sin_relogin(self, cliente, token_admin):
        _crear_usuario(cliente, "revoca@test.com")
        token_usuario = _login(cliente, "revoca@test.com").json()["access_token"]
        headers_usuario = _headers(token_usuario)

        # Popula el cache de estado con rol USUARIO
        resp = cliente.get("/auth/me", headers=headers_usuario)
        assert resp.status_code == 200
        assert resp.json()["roles"] == ["USUARIO"]

        assert cliente.get("/roles/", headers=headers_usuario).status_code == 403

        usuario_id = _login(cliente, "revoca@test.com").json()["id"]
        resp = cliente.post(
            f"/usuarios/{usuario_id}/roles",
            headers=_headers(token_admin),
            json={"id_rol": 1},
        )
        assert resp.status_code == 200

        # Mismo token, sin re-login: el cache se invalidó al asignar rol
        resp = cliente.get("/roles/", headers=headers_usuario)
        assert resp.status_code == 200

    def test_quitar_rol_revoca_sin_relogin(self, cliente, token_admin):
        _crear_usuario(cliente, "quita@test.com")
        token_usuario = _login(cliente, "quita@test.com").json()["access_token"]
        headers_usuario = _headers(token_usuario)

        usuario_id = _login(cliente, "quita@test.com").json()["id"]
        resp = cliente.post(
            f"/usuarios/{usuario_id}/roles",
            headers=_headers(token_admin),
            json={"id_rol": 1},
        )
        assert resp.status_code == 200

        # Popula cache con rol ADMIN
        resp = cliente.get("/auth/me", headers=headers_usuario)
        assert resp.status_code == 200
        assert "ADMIN" in resp.json()["roles"]

        resp = cliente.delete(
            f"/usuarios/{usuario_id}/roles/1", headers=_headers(token_admin)
        )
        assert resp.status_code == 200
        assert 1 not in resp.json()["ids_roles"]

        # Mismo token, sin re-login: el rol ya no autoriza
        resp = cliente.get("/roles/", headers=headers_usuario)
        assert resp.status_code == 403

    def test_usuario_inactivo_con_token_vigente_recibe_401(self, cliente, token_admin):
        _crear_usuario(cliente, "inactiva@test.com")
        token_usuario = _login(cliente, "inactiva@test.com").json()["access_token"]
        headers_usuario = _headers(token_usuario)

        assert cliente.get("/auth/me", headers=headers_usuario).status_code == 200

        usuario_id = _login(cliente, "inactiva@test.com").json()["id"]
        resp = cliente.delete(f"/usuarios/{usuario_id}", headers=_headers(token_admin))
        assert resp.status_code == 200

        resp = cliente.get("/auth/me", headers=headers_usuario)
        assert resp.status_code == 401

        resp = cliente.get("/usuarios/", headers=headers_usuario)
        assert resp.status_code == 401

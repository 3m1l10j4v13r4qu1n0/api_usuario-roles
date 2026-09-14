# Auditoría de Historias de Usuario

> **Fecha:** 2026-09-14
> **Auditor:** Agente de IA (sesión de documentación por ingeniería inversa)
> **Alcance:** Historias de Usuario HU-01..HU-10 vs código real de `api_usuario-roles` (rama `feature/documentacion`, base `develop`).

## 1. Resumen

Las 10 Historias de Usuario se documentaron por **ingeniería inversa** desde el código ya
implementado: cada HU está respaldada por un caso de uso real (`app/application/use_cases/`),
endpoints reales (`app/presentation/routers/`), schemas reales (`app/presentation/schemas/`)
y tests reales (`tests/unit/domian/services/` + `tests/integration/`). **10/10 HUs implementadas
y verificadas**.

## 2. Resultado por HU

| HU | Historia | Endpoint(s) real(es) | Caso de uso | Tests (unit + integración) | Estado |
|---|---|---|---|---|---|
| HU-01 | Login y `/auth/me` | `POST /auth/login` · `GET /auth/me` | `uc1_login.py` | `test_uc1_login.py` (4) + `test_auth_service.py` (8) + `test_flujo_completo.py` (login incorrecto) | ✅ |
| HU-02 | Registrar usuario | `POST /usuarios/` (público, 201) | `uc2_registrar_usuario.py` | `test_uc2_registrar_usuario.py` (10) + `test_autorizacion_roles.py::test_registro_autoasigna_rol_usuario` + `test_flujo_completo.py::test_email_duplicado_devuelve_409` | ✅ |
| HU-03 | Listar usuarios | `GET /usuarios/` (ADMIN) | `uc3_listar_usuarios.py` | `test_uc3_listar_usuarios.py` (2) + `test_autorizacion_roles.py::test_403_sin_rol_admin_...` + `test_flujo_completo.py::test_endpoints_protegidos_sin_token_devuelven_401` | ✅ |
| HU-04 | Obtener usuario por ID | `GET /usuarios/{usuario_id}` (ADMIN o propio) | `uc4_obtener_usuario_por_id.py` | `test_uc4_obtener_usuario_por_id.py` (2) + `test_autorizacion_roles.py` (mismo usuario / 403 cruzado) | ✅ |
| HU-05 | Actualizar usuario | `PATCH /usuarios/{usuario_id}` (ADMIN o propio) | `uc5_actualizar_usuario.py` | `test_uc5_actualizar_usuario.py` (7) | ✅ |
| HU-06 | Baja lógica | `DELETE /usuarios/{usuario_id}` (ADMIN) | `uc6_dar_de_baja_usuario.py` | `test_uc6_dar_de_baja_usuario.py` (3) + `test_flujo_completo.py::test_baja_logica_rechaza_login` + `test_autorizacion_roles.py::test_usuario_inactivo_con_token_vigente_recibe_401` | ✅ |
| HU-07 | Crear rol | `POST /roles/` (ADMIN, 201) | `uc7_crear_rol.py` | `test_uc7_crear_rol.py` (6) + `test_autorizacion_roles.py::test_403_sin_rol_admin_...` | ✅ |
| HU-08 | Listar roles | `GET /roles/` (ADMIN) | `uc8_listar_roles.py` | `test_uc8_listar_roles.py` (3) + `test_flujo_completo.py` (flujo completo) | ✅ |
| HU-09 | Asignar rol | `POST /usuarios/{usuario_id}/roles` (ADMIN) | `uc9_asignar_rol.py` | `test_uc9_asignar_rol.py` (4) + `test_autorizacion_roles.py::test_asignar_rol_se_refleja_sin_relogin` | ✅ |
| HU-10 | Quitar rol | `DELETE /usuarios/{usuario_id}/roles/{rol_id}` (ADMIN) | `uc10_quitar_rol.py` | `test_uc10_quitar_rol.py` (4) + `test_autorizacion_roles.py::test_quitar_rol_revoca_sin_relogin` | ✅ |

## 3. Detalle de lo pendiente

Sin HU pendientes. Pendientes generales **no vinculados a HUs** (ver `docs/estado_actual_proyecto.md` §7):
- Release de `develop` → `main` (decisión del equipo).
- Optional: refresh tokens (hoy solo access token JWT 15 min).
- Scale horizontal: cache in-memory → Redis (`EstadoUsuarioCachePort` listo para el swap).

## 4. Verificaciones operativas

- [x] `venv/bin/ruff check .` — OK.
- [x] `venv/bin/black --check .` — OK.
- [x] `venv/bin/python -m pytest -q` — **75 passed** (unitarios con fakes).
- [x] `venv/bin/python -m pytest tests/integration/` — **13 passed** (BD real).
- [x] Endpoints documentados coinciden con `app/presentation/routers/*.py`.
- [x] Schemas documentados coinciden con `app/presentation/schemas/*.py`.
- [x] Nombres de tests en los planes de prueba coinciden con `tests/`.

## 5. Archivos modificados

- `docs/01_global/` (4 archivos nuevos), `docs/02_tecnico/` (2 md + 14 diagramas),
  `docs/03_procesos/definicion_listo.md`, `docs/04_historias_usuario/HU-01..HU-10/` (50 md),
  `docs/05_metodologia_agil/metodoKanban.md`, este informe.
- `docs/estado_actual_proyecto.md` y `docs/vitacora_agentica.md` se actualizan al cierre.

## 6. Notas de seguimiento

- (2026-09-14) Documentación generada por ingeniería inversa en `feature/documentacion`,
  replicando el formato Benn de `api_normalizacion_afiliados/docs/`. Se corrigió el typo
  heredado `_pruevas.md` → `_pruebas.md`. Renders SVG de PlantUML generados con
  `plantuml.jar` (motor Smetana, sin dependencia de Graphviz).
- (2026-09-14) La HU-10 (quitar rol) se documenta aunque originalmente no figuraba en AGENTS.md:
  el código ya la tiene implementada (UC10) desde la Fase 5.
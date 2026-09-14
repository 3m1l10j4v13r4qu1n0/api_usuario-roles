# Estado Actual del Proyecto

> Última actualización: 2026-09-14
> Este archivo es una FOTO del presente, no un historial. Para el historial de cambios ver `vitacora_agentica.md`.
> El agente debe leer este archivo completo al iniciar cualquier tarea sobre el proyecto.

## 1. Resumen del proyecto

API REST de **autenticación y autorización (usuarios + roles + JWT)** en Python/FastAPI. Es un microservicio del ecosistema mayor descrito en el diagrama de microservicios (Frontend → API REST → servicios), que provee la capa de auth para el resto. Stack: FastAPI + SQLAlchemy 2.0 async (asyncpg) + pydantic-settings + `bcrypt` (hashing) + `PyJWT` (tokens), Python 3.13.5 (`app/.python-version`).

## 2. Arquitectura

Clean Architecture + Hexagonal (Ports & Adapters). El dominio no importa frameworks, ni siquiera `bcrypt` o `PyJWT`.

- `app/domain/` — entidades puras (`Usuario`, `Rol` como dataclasses), servicios (`validacion.py`, `normalizacion.py`, `auth_service.py`) y **ports** (`ABC` + `abstractmethod`): `usuario/`, `rol/`, `authentication/` (`PasswordHasherPort`, `TokenProviderPort`). `exceptions.py` define excepciones de dominio.
- `app/application/use_cases/` — casos de uso `ucN_*.py` (clases `...UseCase` con `async def execute`), reciben ports, no implementaciones.
- `app/infrastructure/` — adapters: ORM + repositorios en `database/`, auth en `auth/` (`BcryptPasswordHasher`, `JwtTokenProvider`), wiring en `dependencies/` (`dependency_injection.py` + `auth_dependencies.py` con `get_current_user` y `require_roles`).
- `app/presentation/` — routers (`auth.py`, `usuarios.py`, `roles.py`), schemas Pydantic y `handlers.py` (mapea excepciones de dominio → HTTP, payload `{"error": str(exc)}`).

Convenciones claves: todo caso de uso se cablea en `dependency_injection.py` y se inyecta con `Depends`; los endpoints protegidos inyectan `get_current_user`; `get_db()` hace commit automático al final del request (los casos de uso no commitean).

## 3. Entidades / Modelos de dominio

- `Usuario` — datos de acceso del usuario (nombre_usuario, email único, password_hash) + baja lógica (activo) + `ids_roles`.
- `Rol` — rol del sistema (nombre único, descripcion).
- `EstadoUsuario` — estado del usuario autenticado que la autorización necesita (usuario_id, email, nombre_usuario, activo, roles). Se cachea por TTL corto (patrón híbrido).

## 4. Casos de uso / Servicios implementados

- [x] UC1 — Login con JWT (`uc1_login.py`, `LoginUseCase`) — emite token con `sub` (id) y `roles`.
- [x] UC2 — Registrar usuario (`uc2_registrar_usuario.py`) — hashea la contraseña, norma email a minúsculas, rechaza duplicados y **autoasigna el rol `USUARIO`**.
- [x] UC3 — Listar usuarios (`uc3_listar_usuarios.py`).
- [x] UC4 — Obtener usuario por ID (`uc4_obtener_usuario_por_id.py`).
- [x] UC5 — Actualizar usuario (`uc5_actualizar_usuario.py`) — solo campos presentes; rehashea si cambia password; valida email duplicado.
- [x] UC6 — Dar de baja usuario (`uc6_dar_de_baja_usuario.py`) — baja lógica (`activo=False`) + invalida estado del usuario en cache.
- [x] UC7 — Crear rol (`uc7_crear_rol.py`).
- [x] UC8 — Listar roles (`uc8_listar_roles.py`).
- [x] UC9 — Asignar rol a usuario (`uc9_asignar_rol.py`) + invalida estado del usuario en cache.
- [x] UC10 — Quitar rol a usuario (`uc10_quitar_rol.py`) + invalida estado del usuario en cache.

Servicios de dominio puros: `validacion.py` (RN04 email, RN05 campos obligatorios, RN06 password ≥ 8), `normalizacion.py` (RN01 email en minúsculas, RN02 trim), `auth_service.py` (`verificar_credenciales`, `autorizar`).

## 5. Endpoints / Interfaces expuestas

| Método | Ruta | Descripción | Estado |
|---|---|---|---|
| POST | `/auth/login` | Autentica y devuelve token JWT (UC1) | ✅ funcionando contra BD real |
| GET | `/auth/me` | Usuario autenticado desde el token | ✅ funcionando contra BD real |
| POST | `/usuarios/` | Registrar usuario (UC2) — público, autoasigna USUARIO | ✅ funcionando contra BD real |
| GET | `/usuarios/` | Listar usuarios (UC3) — JWT + ADMIN | ✅ funcionando contra BD real |
| GET | `/usuarios/{usuario_id}` | Obtener usuario (UC4) — ADMIN o el propio usuario | ✅ funcionando contra BD real |
| PATCH | `/usuarios/{usuario_id}` | Actualizar usuario (UC5) — ADMIN o el propio usuario | ✅ funcionando contra BD real |
| DELETE | `/usuarios/{usuario_id}` | Baja lógica (UC6) — JWT + ADMIN | ✅ funcionando contra BD real |
| POST | `/usuarios/{usuario_id}/roles` | Asignar rol (UC9) — JWT + ADMIN (cuerpo: `{"id_rol": N}`) | ✅ funcionando contra BD real |
| DELETE | `/usuarios/{usuario_id}/roles/{rol_id}` | Quitar rol (UC10) — JWT + ADMIN | ✅ funcionando contra BD real |
| POST | `/roles/` | Crear rol (UC7) — JWT + ADMIN | ✅ funcionando contra BD real |
| GET | `/roles/` | Listar roles (UC8) — JWT + ADMIN | ✅ funcionando contra BD real |
| GET | `/` | Health check | ✅ |

## 6. Infraestructura / Integraciones

- PostgreSQL async (`DATABASE_URL`, var obligatoria). **Alembic con migración inicial aplicada** (`9378f376749f_crear_tablas_usuarios_roles`) → tablas `usuarios`, `roles`, `usuario_roles` creadas en BD real `auth_db`.
- Seguridad: `bcrypt==4.3.0` (`app/infrastructure/auth/password_hasher.py`), `PyJWT==2.10.1` (`app/infrastructure/auth/jwt_token_provider.py`), `cachetools==6.0.0` (`app/infrastructure/cache/estado_usuario_cache_memoria.py`). Variables `JWT_SECRET_KEY` (obligatoria), `JWT_ALGORITHM` (HS256), `JWT_EXPIRATION_MINUTES` (15 por defecto), `AUTH_CACHE_TTL_SEGUNDOS` (60), `AUTH_CACHE_MAX_ITEMS` (1000).
- **Autorización por rol (Fase 5)**: patrón híbrido — JWT corto (identidad) + cache de estado por `user_id` (activo + roles) con TTL 60s. `get_current_user` resuelve el estado real desde el cache y, en miss, desde la BD (no confía en las claims del token). Asignar/quitar rol y dar de baja invalidan el cache → **la revocación se refleja sin re-login**.
- Matriz de roles aplicada a los endpoints de `/usuarios/*`: listar/baja/asignar/quitar rol solo `ADMIN`; obtener/actualizar `ADMIN` o el propio usuario (dependencia `require_mismo_usuario_o_admin`); el registro queda público y autoasigna `USUARIO`. `/roles/*` sigue siendo solo `ADMIN`.
- Bootstrap en tests de integración: se crea un usuario `admin@bootstrap.com` (rol ADMIN) y se recrea en cada test, porque las operaciones de rol requieren ADMIN y la limpieza borra `usuarios`.
- CORS configurado con `CORS_ORIGINS` (default localhost:5173/3000).
- `requirements.txt` en `app/requirements.txt` (no en la raíz).
- Seed de roles iniciales ejecutado contra BD real (`python -m app.infrastructure.database.seed_runner`) → roles `ADMIN` y `USUARIO` presentes (id 1 y 2). Re-ejecutar es idempotente (no inserta si la tabla tiene filas).
- Fix de repositorios (SQLAlchemy async): queries usan `selectinload(UsuarioORM.roles)` y los comandos refrescan la relación + `UsuarioORM` usa `mapper_args = {"eager_defaults": True}` (recupera `fecha_actualizacion` por `RETURNING` y evita `MissingGreenlet`). `crear` asocia los roles de `usuario.ids_roles`.
- ORM models declarados con estilo SQLAlchemy 2.0 `Mapped` + `mapped_column` (evita falsos positivos de Pylance/mypy). La tabla asociativa `usuario_roles` se mantiene como `Table` de core.
- Tests puros desacoplados de `DATABASE_URL` vía `tests/conftest.py`. `pytest`: 75 pasando (dominio + casos de uso UC1..UC10), `ruff` y `black` en verde.
- Tests de integración en `tests/integration/` (marcador `integracion`, excluidos por defecto vía `addopts --ignore`): corren con `python -m pytest tests/integration/` contra la BD real del `.env`. 13/13 en verde (flujo completo + autorización por rol + errores 401/403/409).

## 7. Pendientes / TODO conocidos

✅ **Fase 5 (autorización por rol) completada en `feature/autorizacion-roles`.** Se definió y aplicó la matriz de roles sobre `/usuarios/*`, se agregó el UC10 (quitar rol), el registro autoasigna `USUARIO`, y se adoptó el patrón híbrido (JWT corto + cache de estado con TTL) con revocación en caliente. Pendientes residuales:

1. ~~Decidir roles de autorización por endpoint~~ ✅ resuelto (ver §6: matriz aplicada).
2. ~~Decidir si `POST /usuarios/` queda público o requiere ADMIN~~ ✅ queda **público** (decisión del equipo, revisitable).
3. ~~Revisar si `get_current_user` debe verificar `activo`~~ ✅ ahora `get_current_user` resuelve el estado real (activo + roles) desde cache/BD y **rechaza inactivos con 401**.
4. ~~Observado: roles fijos hasta re-login~~ ✅ resuelto por el patrón híbrido: asignar/quitar rol o dar de baja invalidan el cache y el cambio se refleja en el próximo request sin re-login.
5. Si se escala horizontalmente, el cache in-memory debe reemplazarse por Redis (el port `EstadoUsuarioCachePort` soporta el cambio).
6. Refresh token: hoy solo access token JWT (corto, 15 min). Decidir si hace falta en una fase futura.
7. **Release a `main`** pendiente: `main` quedó atrasado respecto de `develop`. La Fase 6 se cerró de forma **documental** (sin release). Se creó la rama `feature/fase-6-cierre` desde `develop` (reutilizable) para cuando se decida mergear o hacer release.

## 8. Decisiones y convenciones vigentes

- Comandos siempre desde la raíz del repo (imports `app.*`, nunca desde `app/`); no repetir `alembic init`.
- `requirements.txt` en `app/requirements.txt`; no hay venv commitado; `tests/conftest.py` setea `DATABASE_URL` por defecto.
- `arquitectura`: dominio puro estricto (ni `bcrypt`/`PyJWT` en `app/domain/`). Los adapters de auth viven en `app/infrastructure/auth/`.
- `baja lógica` de usuario = `activo=False` (no se borra físicamente). El login rechaza usuarios inactivos.
- `payload de errores` unificado: todas las excepciones de dominio usan `{"error": str}`. Mapeo: 401 (credenciales/token), 403 (rol), 404 (no encontrado), 409 (email duplicado), 422 (datos inválidos).
- El directorio de tests de dominio es `tests/unit/domian/` (tipeo original heredado de `api_normalizacion_afiliados`).
- Reglas y skills traídos y adaptados de `api_normalizacion_afiliados`: `.agents/rules/*` y `.agents/skills/*` (`di-architect-scaffold`, `estado-actual-proyecto`, `vitacora-agentica`, `rest-api-design`, `apa-software-doc`, `pdf-to-markdown`).
- Al terminar trabajo relevante, actualizar este archivo (in-place) y agregar entrada a `vitacora_agentica.md` (append-only).
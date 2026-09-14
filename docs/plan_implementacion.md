# Plan de Implementación — api_usuario-roles

> Referencia única para el trabajo por fases. Al terminar cada fase, taggear con semver (`v1.0.0`, `v1.1.0`, …).
> No pushear rama ni tag sin aprobación explícita del usuario.

---

## Fase 1 — Andamiaje ✅ completada

Crear la arquitectura base del microservicio reutilizando patrones de `api_normalizacion_afiliados` y adaptando skills/rules.

### Entregables
- [x] Crear árbol de carpetas `app/` (domain, application, infrastructure, presentation)
- [x] Crear `config.py` con `DATABASE_URL` + JWT vars
- [x] Crear `connection.py` (async, `get_db()` con commit automático)
- [x] Crear `requirements.txt` (fastapi + sqlalchemy + asyncpg + bcrypt + PyJWT)
- [x] Crear `main.py` (lifespan, CORS, handlers, routers)
- [x] Crear dominio puro: `exceptions.py`, `models/usuario.py`, `models/rol.py`
- [x] Crear servicios de dominio: `normalizacion.py`, `validacion.py`, `auth_service.py`
- [x] Crear ports: `PasswordHasherPort`, `TokenProviderPort`, ports de usuario y rol
- [x] Crear 9 casos de uso (UC1..UC9)
- [x] Crear ORM models: `UsuarioORM`, `RolORM`, tabla `usuario_roles`
- [x] Crear repositorios (query + command para usuario y rol)
- [x] Crear adapters de auth: `BcryptPasswordHasher`, `JwtTokenProvider`
- [x] Crear DI: `dependency_injection.py`, `auth_dependencies.py` (`get_current_user`, `require_roles`)
- [x] Crear routers: `auth.py`, `usuarios.py`, `roles.py`
- [x] Crear schemas: `auth_schema.py`, `usuario_schema.py`, `rol_schema.py`
- [x] Crear `handlers.py` (excepciones → HTTP)
- [x] Crear seed de roles iniciales (`seed.py` + `seed_runner.py`)
- [x] Crear tests de dominio: normalización, validación, auth_service, UC1 login (fakes)
- [x] Adaptar skills y rules de `api_normalizacion_afiliados`
- [x] Crear AGENTS.md

### Notas
- `POST /usuarios/` queda público por ahora para permitir el alta inicial de usuarios. Decidir con el equipo si cambiarlo a autenticado + rol ADMIN.

---

## Fase 2 — Base de datos real ✅ completada

### Entregables
- [x] Instalar venv: `python -m venv venv && . venv/bin/activate && pip install -r app/requirements.txt`
- [x] Configurar `.env` con `DATABASE_URL` real y `JWT_SECRET_KEY` segura
- [x] Correr `alembic revision --autogenerate -m "crear_tablas_usuarios_roles"`
- [x] Revisar la migración generada (verificar tipos: `String(255)` para email/hash, `Boolean` para activo, `DateTime` para timestamps, PK compuesta de `usuario_roles`)
- [x] Correr `alembic upgrade head`
- [x] Correr `python -m app.infrastructure.database.seed_runner` → debe insertar ADMIN y USUARIO
- [x] Probar manual: `GET /` → health check, `POST /usuarios/` → crear usuario, `POST /auth/login` → obtener token

### Notas
- Durante la prueba manual se encontró y corrigió un bug de repositorios async: `MissingGreenlet` al acceder a `orm.roles` y a defaults del servidor tras `flush`. Fix: `selectinload` explícito en queries, refresh de relaciones tras comandos y `eager_defaults=True` en `UsuarioORM`.
- El flujo real completo (crear → login → asignar rol ADMIN → re-login → listar roles → crear rol → baja lógica → login rechazado de usuario inactivo → email duplicado 409) quedó verificado manualmente contra BD real.

---

## Fase 3 — Tests unitarios UC2..UC9 ✅ completada

### Entregables
- [x] `test_uc2_registrar_usuario.py` — test de creación exitosa + duplicado + datos inválidos
- [x] `test_uc3_listar_usuarios.py`
- [x] `test_uc4_obtener_usuario_por_id.py`
- [x] `test_uc5_actualizar_usuario.py` — test email duplicado + password nueva
- [x] `test_uc6_dar_de_baja_usuario.py`
- [x] `test_uc7_crear_rol.py` — test duplicado
- [x] `test_uc8_listar_roles.py`
- [x] `test_uc9_asignar_rol.py` — test usuario no existe + rol no existe
- [x] Verificar que `pytest` pasa todo desde la raíz (67 passed: 34 previos + 33 nuevos)

### Notas
- Fakes en memoria locales por archivo, siguiendo el patrón de `test_uc1_login.py`.
- UC5 se testea con un stub que replica `model_dump(exclude_unset=True)`, aislando el dominio de Pydantic.
- Los usuarios/roles usados en los tests se crean con factories (no singletons de módulo) para evitar contaminación entre tests por mutación.

---

## Fase 4 — Test de integración real ✅ completada

### Entregables
- [x] Test de login completo contra BD real (flujos happy path + error)
- [x] Test de `POST /usuarios/` → `POST /auth/login` → `GET /auth/me` → `POST /usuarios/{id}/roles` → `GET /roles/`
- [x] Correr `ruff check .` y `black --check .` sin errores

### Notas
- Se creó `tests/integration/` con el marcador `integracion`. Los tests se excluyen por defecto vía `addopts = "--ignore=tests/integration"` en `pyproject.toml`; correr con `python -m pytest tests/integration/`.
- Usan `TestClient` de FastAPI contra la BD real del `.env`. El engine de la app solo vive dentro del loop del `TestClient`; el ping y la limpieza de estado usan engines descartables propios para evitar el error "Future attached to a different loop" (los event loops no se comparten).
- La limpieza posterior a cada test borra `usuario_roles`, `usuarios` y los roles no seed (preserva `ADMIN`/`USUARIO`), garantizando tests idempotentes.
- Se asume el seed corrido: el rol `ADMIN` tiene id 1 y se usa para las pruebas de autorización.

---

## Fase 5 — Autorización por rol ✅ completada

### Entregables
- [x] Definir, con el equipo, qué endpoints exigen qué roles
- [x] Agregar `Depends(require_roles(...))` según lo decidido
- [x] Test de autorización (403 si no tiene el rol)

### Notas
- **Matriz aplicada** (`app/presentation/routers/usuarios.py`): `GET /usuarios/` → ADMIN; `GET/PATCH /usuarios/{id}` → ADMIN o el propio usuario (`require_mismo_usuario_o_admin`); `DELETE /usuarios/{id}` → ADMIN; `POST /usuarios/{id}/roles` → ADMIN; nuevo `DELETE /usuarios/{id}/roles/{rol_id}` (UC10) → ADMIN. `POST /usuarios/` queda **público** y ahora **autoasigna el rol `USUARIO`**. `/roles/*` sigue exigiendo ADMIN.
- **Patrón híbrido adoptado** (decisión del equipo): access token JWT corto (default `JWT_EXPIRATION_MINUTES=15`) + cache de estado por `user_id` (activo + roles, TTL 60s, `cachetools`) en `EstadoUsuarioCachePort`. `get_current_user` resuelve el estado real (cache → BD en miss) y verifica `activo`. UC6/UC9/UC10 invalidan el cache al cambiar roles/baja → **revocación en caliente sin re-login**.
- Tests de integración: `tests/integration/test_autorizacion_roles.py` (403 por rol, ownership, revocación en caliente con asignar/quitar rol, usuario inactivo con token vivo → 401). El conftest bootstrapa `admin@bootstrap.com` con rol ADMIN porque las operaciones de rol exigen ADMIN.
- `pytest` 75 unit + 13 integración, `ruff` y `black` en verde.

---

## Fase 6 — Cierre ✅ completada (cierre documental)

### Entregables
- [x] Tag `v1.0.0` (o `v1.x.0` según se hay hecho correcciones) — cierre de fases: `v1.0.0`…`v1.3.0` (última fase cerrada con tag `v1.3.0`, pusheado)
- [x] Actualizar `docs/estado_actual_proyecto.md`
- [x] Verificar que todos los tests pasan — 75 unit + 13 integración contra BD real
- [x] Merge a develop (si se trabajó en feature branch) — `84a93b6` (merge de `feature/autorizacion-roles`), pusheado

### Notas
- Cierre **documental** (decisión del usuario): no se generó tag extra de cierre ni release a `main`. `main` quedó atrasado respecto de `develop`, pendiente (no es bloqueante; el microservicio está completo y verificado en `develop`).
- Operaciones git del cierre: merge `feature/autorizacion-roles` → `develop` (`84a93b6`), tag `v1.3.0`, push de `develop` y del tag, y limpieza de ramas ya mergeadas (locales + remotas; quedó `origin/feature/docs-readme` porque es la rama default de GitHub).
- Rama de ambientes: se creó `feature/fase-6-cierre` desde `develop` para el cierre; puede reusarse o descartarse para próximas fases.

---

## Decisiones pendientes

| # | Pregunta | Estado |
|---|---|---|
| 1 | ¿`POST /usuarios/` debe ser público o requiere ADMIN? | ✅ Público (decisión del equipo, revisitable) |
| 2 | ¿Qué roles hay además de ADMIN y USUARIO? | ✅ Siguen ADMIN y USUARIO (USUARIO ahora se autoasigna en el alta) |
| 3 | ¿`GET /usuarios/` y `GET /usuarios/{id}` requieren ser el mismo usuario o ADMIN? | ✅ Listar → ADMIN; obtener/actualizar → ADMIN o el propio usuario |
| 4 | ¿`DELETE /usuarios/{id}` requiere ser ADMIN? | ✅ Sí |
| 5 | ¿`POST /usuarios/{id}/roles` debe ser solo ADMIN? (hoy es público con JWT) | ✅ Sí (y se agregó `DELETE .../roles/{rol_id}`, UC10, solo ADMIN) |
| 6 | ¿Se necesita refresh token o solo access token? | ⏳ Pendiente — hoy solo access token JWT corto (15 min) |

Cada decisión actualiza este archivo y `docs/estado_actual_proyecto.md`.
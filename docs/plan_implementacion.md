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

## Fase 4 — Test de integración real ⏳ pendiente

### Entregables
- [ ] Test de login completo contra BD real (flujos happy path + error)
- [ ] Test de `POST /usuarios/` → `POST /auth/login` → `GET /auth/me` → `POST /usuarios/{id}/roles` → `GET /roles/`
- [ ] Correr `ruff check .` y `black --check .` sin errores

---

## Fase 5 — Autorización por rol ⏳ pendiente

### Entregables
- [ ] Definir, con el equipo, qué endpoints exigen qué roles (hoy solo `/roles/*` exige ADMIN)
- [ ] Agregar `Depends(require_roles(...))` según lo decidido
- [ ] Test de autorización (403 si no tiene el rol)

---

## Fase 6 — Cierre ⏳ pendiente

### Entregables
- [ ] Tag `v1.0.0` (o `v1.x.0` según se hay hecho correcciones)
- [ ] Actualizar `docs/estado_actual_proyecto.md`
- [ ] Verificar que todos los tests pasan
- [ ] Merge a develop (si se trabajó en feature branch)

---

## Decisiones pendientes

| # | Pregunta | Estado |
|---|---|---|
| 1 | ¿`POST /usuarios/` debe ser público o requiere ADMIN? | Pendiente |
| 2 | ¿Qué roles hay además de ADMIN y USUARIO? | Pendiente |
| 3 | ¿`GET /usuarios/` y `GET /usuarios/{id}` requieren ser el mismo usuario o ADMIN? | Pendiente |
| 4 | ¿`DELETE /usuarios/{id}` requiere ser ADMIN? | Pendiente |
| 5 | ¿`POST /usuarios/{id}/roles` debe ser solo ADMIN? (hoy es público con JWT) | Pendiente |
| 6 | ¿Se necesita refresh token o solo access token? | Pendiente |

Cada decisión actualiza este archivo y `docs/estado_actual_proyecto.md`.
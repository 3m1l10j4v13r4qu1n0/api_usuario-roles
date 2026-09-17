# Vitácora Agéntica

> Historial cronológico y append-only. NUNCA se borra ni se reescribe una entrada pasada.
> Cada entrada corresponde a una sesión/tarea significativa de trabajo del agente sobre el proyecto.
> Cuando este archivo crezca demasiado, archivar entradas viejas en `vitacora_YYYY-QX.md` y dejar acá solo un índice + las últimas entradas.

---

## 2026-09-11 — Scaffolding completo del microservicio api_usuario-roles

**Qué se hizo:** se creó la arquitectura base completa del nuevo microservicio de usuarios y roles con JWT desde cero, reutilizando patrones y skills de `api_normalizacion_afiliados`. Se crearon: dominio puro (Usuario, Rol, ports de auth), 9 casos de uso (UC1..UC9), ORM models, repositorios, adapters de auth (bcrypt + PyJWT), dependencias de DI + auth_dependencies (get_current_user, require_roles), routers (auth, usuarios, roles), schemas Pydantic, handlers, seed de roles, tests de dominio (normalización, validación, auth_service, UC1 login con fakes), AGENTS.md, y documentación (estado_actual_proyecto.md, plan_implementacion.md).

**Decisiones de arquitectura:**
- Dominio estrictamente puro: ni `bcrypt` ni `PyJWT` se importan en `app/domain/`; los ports `PasswordHasherPort` y `TokenProviderPort` viven en `app/domain/ports/authentication/` y los adapters en `app/infrastructure/auth/`.
- Baja lógica de usuario: `activo=False` (no se borra físicamente), coherente con la baja lógica de `api_normalizacion_afiliados`.
- `POST /usuarios/` queda público para permitir el alta inicial; decidir con el equipo si protegerlo.
- Seed de roles: `ADMIN` y `USUARIO` (tabla `roles`).
- Port de RolQuery con método `obtener_nombres_por_ids` para resolver nombres de roles del token JWT en el UC1 login.
- Directorio de tests hereda el typo `tests/unit/domian/` del proyecto original.
- `require_roles(*roles_requeridos)` es una fábrica de dependencias que usa `autorizar` del dominio.

**Archivos/módulos tocados:**
- `app/domain/exceptions.py` — 7 excepciones de dominio (UsuarioNoEncontradoError, RolNoEncontradoError, DatoInvalidoError, EmailDuplicadoError, CredencialesInvalidasError, TokenInvalidoError, NoAutorizadoError)
- `app/domain/models/usuario.py`, `app/domain/models/rol.py` — entidades puras dataclass
- `app/domain/services/normalizacion.py`, `validacion.py`, `auth_service.py` — servicios de dominio
- `app/domain/ports/` — 6 ports: usuario_command, usuario_query, rol_command, rol_query, password_hasher, token_provider
- `app/application/use_cases/uc1_login.py` … `uc9_asignar_rol.py` — 9 casos de uso
- `app/infrastructure/core/config.py` — Settings con JWT vars
- `app/infrastructure/database/connection.py`, `orm_models/`, `repositories/`, `seed.py`, `seed_runner.py`
- `app/infrastructure/auth/password_hasher.py`, `jwt_token_provider.py`
- `app/infrastructure/dependencies/dependency_injection.py`, `auth_dependencies.py`
- `app/presentation/handlers.py`, `routers/auth.py`, `usuarios.py`, `roles.py`, `schemas/auth_schema.py`, `usuario_schema.py`, `rol_schema.py`
- `app/main.py` — CORS, lifespan, handlers, routers
- `AGENTS.md`, `docs/estado_actual_proyecto.md`, `docs/plan_implementacion.md`
- `.agents/rules/` — 7 reglas adaptadas (flujo-git, versionado, reglas-solid, auditoria, anti-alucinación, formato APA)
- `.agents/skills/di-architect-scaffold/SKILL.md` — reescrito para el nuevo proyecto
- `.agents/skills/rest-api-design/references/fastapi-conventions.md`, `templates/endpoint_fastapi.py` — adaptados

**Estado resultante:** andamiaje completo, código listo pero sin migración de Alembic, sin BD real, sin venv instalado, y tests de dominio creados (pendiente correr `pytest` con dependencias instaladas). Ver `docs/plan_implementacion.md` Fase 2 para los próximos pasos.

---

## 2026-09-14 — Fase 2 completada: BD real, migración Alembic, seed y fix de repositorios async

**Qué se hizo:** se completó la Fase 2 del plan (base de datos real). El usuario configuró `.env` y creó la BD `auth_db`. Se generó y aplicó la migración inicial de Alembic (`9378f376749f_crear_tablas_usuarios_roles`) creando `usuarios`, `roles` y `usuario_roles`; se corrió el seed (`ADMIN` y `USUARIO`); y se probó el flujo real completo por HTTP (crear usuario → login → asignar rol → re-login → listar/crear roles → baja lógica → login rechazado de inactivo → email duplicado 409 → 403 sin rol ADMIN).

**Decisiones/acciones:**
- Rama de trabajo: `feature/migracion-bd` creada desde `develop` (una rama = una tarea; no se siguió en `feature/docs-readme`).
- **Fix bug `MissingGreenlet`** en repositorios async: acceder a `orm.roles` sobre objetos recién creados o a defaults del servidor expirados tras `flush` rompía en contexto async. Solución:
  - `usuario_query_repository.py`: helper `_query_con_roles()` con `selectinload(UsuarioORM.roles)` para `listar`, `obtener_por_id`, `obtener_por_email`.
  - `usuario_command_repository.py`: helpers con `selectinload` para `buscar_por_email*` y `_refresh_con_roles()` (refresh de `roles`) tras `crear`/`actualizar`/`dar_de_baja`/`asignar_rol`.
  - `usuario_orm.py`: `__mapper_args__ = {"eager_defaults": True}` anotado como `ClassVar` → recupera `fecha_actualizacion` por `RETURNING` en UPDATE y evita el expiry de defaults del servidor.
- La migración autogenerada se normalizó con `ruff --fix` y `black` para pasar el checklist.
- Los datos de prueba se limpiaron al final (usuario de prueba eliminado, rol OPERADOR de prueba eliminado); queda la BD con solo los roles del seed.
- Hallazgo de diseño JWT stateless: los roles van en los claims del token al emitirse; asignar/quitar roles exige re-login (registrado en estado_actual_proyecto.md, pendiente de decisión si se cambia a consultar roles desde BD en `get_current_user`).

**Archivos/módulos tocados:**
- `alembic/versions/9378f376749f_crear_tablas_usuarios_roles.py` — migración inicial (generada + reformateada)
- `app/infrastructure/database/repositories/usuario_query_repository.py` — `selectinload` explícito
- `app/infrastructure/database/repositories/usuario_command_repository.py` — `selectinload` + refresh de relaciones
- `app/infrastructure/database/orm_models/usuario_orm.py` — `eager_defaults=True`
- `docs/estado_actual_proyecto.md`, `docs/plan_implementacion.md` — actualizados (Fase 2 completada)

**Estado resultante:** Fase 2 cerrada. BD real `auth_db` con esquema creado y roles seedados. Flujo HTTP completo verificado manualmente. Checklist en verde (`ruff`/`black`/`pytest` 34 passed). Siguiente: Fase 3 (tests unitarios UC2..UC9 con fakes) y Fase 4 (test de integración real).

---

## 2026-09-14 — Refactor ORM models a estilo SQLAlchemy 2.0 (`Mapped` + `mapped_column`)

**Qué se hizo:** por feedback de Pylance (falsos positivos `reportArgumentType`: `Column[int]` no asignable a `int | None`), se migraron los modelos ORM declarativos del estilo SQLAlchemy 1.x (`Column(...)`) al estilo 2.0 (`Mapped[T]` + `mapped_column`), que resuelve los tipos correctamente (`UsuarioORM.id` se ve como `int` en contexto de instancia).

**Decisiones/acciones:**
- `usuario_orm.py`: `id`, `nombre_usuario`, `email`, `password_hash`, `nombre_completo`, `activo`, `fecha_creacion`, `fecha_actualizacion` pasan a `Mapped[...]` con `mapped_column`. La relación `roles` se tipa como `Mapped[list[RolORM]]` (import directo de `rol_orm` en vez de string forward-ref, sin circularidad). Se conserva `lazy="selectin"` y `__mapper_args__ = {"eager_defaults": True}`.
- `rol_orm.py`: `id`, `nombre`, `descripcion` a `Mapped` + `mapped_column`. La tabla asociativa `usuario_roles_table` se mantiene como `Table`/`Column` de core SQLAlchemy (patrón correcto para asociativa; no genera el falso positivo).
- `nullable` ahora se infiere del tipo: `Mapped[str]` → NOT NULL, `Mapped[str | None]` → NULL (mismo esquema que antes).
- Verificación de no-regresión: `alembic check` → "No new upgrade operations detected" (el esquema en BD no cambió), `pytest` 34 passed, `ruff`/`black` en verde, y smoke test HTTP real (crear usuario → login → `/auth/me`) OK.

**Archivos/módulos tocados:**
- `app/infrastructure/database/orm_models/usuario_orm.py` — migrate a `Mapped`/`mapped_column`
- `app/infrastructure/database/orm_models/rol_orm.py` — migrate a `Mapped`/`mapped_column`

**Estado resultante:** ORM models 100% estilo SQLAlchemy 2.0 con tipos correctos para Pylance/mypy. Checklist en verde, esquema de BD intacto, flujo real verificado.

---

## 2026-09-14 — Fase 3: tests unitarios UC2..UC9 con fakes

**Qué se hizo:** se implementaron los tests unitarios de los 8 casos de uso restantes (UC2 a UC9) en `tests/unit/domian/services/`, siguiendo el patrón de `test_uc1_login.py` (fakes en memoria por archivo, `asyncio.run`, clases de test, docstring de cabecera).

**Decisiones/acciones:**
- Archivos creados: `test_uc2_registrar_usuario.py`, `test_uc3_listar_usuarios.py`, `test_uc4_obtener_usuario_por_id.py`, `test_uc5_actualizar_usuario.py`, `test_uc6_dar_de_baja_usuario.py`, `test_uc7_crear_rol.py`, `test_uc8_listar_roles.py`, `test_uc9_asignar_rol.py`.
- UC5 recibe un schema Pydantic (`model_dump(exclude_unset=True)`); se usa un stub `StubUpdate` que replica esa API para mantener el dominio puro (sin Pydantic en tests de dominio).
- Se detectó y corrigió contaminación entre tests por objetos compartidos a nivel de módulo que se mutaban en cada test (usuarios/roles): se resolvió con funciones factory (`usuario_base()`, `usuario_activo()`, `usuario_sin_roles()`) en vez de constantes.
- También se corrigió un fixture de UC2 cuyo email existente no coincidía con el email normalizado de los datos de prueba (el duplicado real no se disparaba).
- Cobertura por UC: registración (éxito, duplicado con/sin mayúsculas, email inválido, password corta, nombre vacío), listar usuarios/roles (vacío + con datos), obtener por id (existe + inexistente → `UsuarioNoEncontradoError`), actualizar (campos, email normalizado, password → hash, email en uso → `EmailDuplicadoError`, mismo email OK, usuario inexistente, sin campos), baja lógica (activo=False + inexistente), crear rol (éxito, sin descripción, normalización, vacío/faltante → `DatoInvalidoError`, duplicado), asignar rol (éxito, rol inexistente → `RolNoEncontradoError`, usuario inexistente → `UsuarioNoEncontradoError`).

**Archivos/módulos tocados:**
- `tests/unit/domian/services/test_uc{2..9}_*.py` — 8 archivos nuevos

**Estado resultante:** Fase 3 completa. `pytest` 67 passed (34 previos + 33 nuevos), `ruff` y `black` en verde. Pendiente: Fase 4 (test de integración real) y Fase 5 (autorización por rol).

---

## 2026-09-14 — Fase 4: test de integración real contra BD

**Qué se hizo:** se implementaron los tests de integración que recorren la API completa (routers + BD real PostgreSQL) con `TestClient` de FastAPI.

**Decisiones/acciones:**
- Nuevo directorio `tests/integration/` con `conftest.py` (cliente session, verificación de BD real con skip automático si no hay conexión, limpieza de estado por test) y `test_flujo_completo.py` (5 tests).
- Se excluyen los tests de integración del `pytest` por defecto vía `addopts = "--ignore=tests/integration"` en `pyproject.toml` (`[tool.pytest.ini_options]`), con marker `integracion` registrado. Correr con `python -m pytest tests/integration/`.
- **Gotcha de event loops resuelto:** `TestClient` corre la app en su propio event loop; usar el `engine` global de `connection.py` tanto dentro (`get_db`) como fuera (`asyncio.run` del ping/limpieza) provocaba `RuntimeError: Task got Future attached to a different loop`. Solución: el ping y la limpieza usan engines descartables (`create_async_engine`) que se crean y destruyen en cada `asyncio.run`, sin compartir conexiones con el loop del cliente.
- **Idempotencia:** la limpieza posterior a cada test borra `usuario_roles`, `usuarios` y los roles no seed (preservando `ADMIN`/`USUARIO`), para que la corrida repetida no falle por roles residuales como `OPERADOR`.
- Tests: flujo completo (registrar → login → `/auth/me` → asignar rol ADMIN id=1 → re-login con rol en token → listar roles → crear rol → listar), baja lógica que rechaza login (401), password incorrecta (401), email duplicado (409), endpoints protegidos sin token (401).

**Archivos/módulos tocados:**
- `tests/integration/__init__.py`, `tests/integration/conftest.py`, `tests/integration/test_flujo_completo.py` — nuevos
- `pyproject.toml` — `[tool.pytest.ini_options]` con `addopts` y marker `integracion`

**Estado resultante:** Fase 4 completa. Integración 5/5 en verde contra BD real (verificado con 3 corridas consecutivas), unitarios 67/67, `ruff` y `black` en verde. Pendiente: Fase 5 (autorización por rol, requiere decisiones del equipo) y Fase 6 (cierre).

---

## 2026-09-14 — Fix post-tag v1.0.1: anotación de `__mapper_args__` en UsuarioORM

**Qué se hizo:** por feedback de Pylance (`reportIncompatibleVariableOverride`), se corrigió la anotación de `__mapper_args__` en `usuario_orm.py`. El `ClassVar[dict]` anterior entraba en conflicto con la variable de instancia del mismo nombre declarada por `DeclarativeBase` (clase base de SQLAlchemy 2.0).

**Decisiones/acciones:**
- Se reemplazó `__mapper_args__: ClassVar[dict] = {"eager_defaults": True}` por `__mapper_args__: dict[str, Any] = {"eager_defaults": True}  # noqa: RUF012`.
- El `# noqa: RUF012` exime la regla de ruff (mutable default en atributo de clase) porque `__mapper_args__` es un atributo especial del mapper que SQLAlchemy consume como configuración estática; no aplica la convención de `ClassVar`.
- Regla práctica registrada: en SQLAlchemy 2.0 con `DeclarativeBase`, los atributos especiales (`__tablename__`, `__mapper_args__`, `__table_args__`) no deben anotarse como `ClassVar`; el `ClassVar` queda reservado para atributos propios de configuración ajenos a la API de SQLAlchemy.
- Sin cambio de comportamiento en runtime; solo tipado. Tag `v1.0.1` (patch post-tag v1.0.0, según regla de versionado).

**Archivos/módulos tocados:**
- `app/infrastructure/database/orm_models/usuario_orm.py` — anotación de `__mapper_args__`

**Estado resultante:** Pylance/mypy sin conflicto de anulación. Checklist en verde (`ruff`/`black`/`pytest` 34 passed, `alembic check` sin cambios de esquema). Commit `4fb4e7c`, tag `v1.0.1` pusheado.

---

## 2026-09-14 — Recordatorio: arranque de Fase 5 (autorización por rol)

**Qué se hizo:** se cerró la Fase 4 (merge `c0aaba8` de `feature/tests-integracion` a `develop`, pusheado) y se creó la rama `feature/autorizacion-roles` desde `develop` para comenzar la Fase 5. También se commiteó el fix de tipado (`b794a6b`, `fix(domain): corregir tipado de normalizacion y validacion de email`) con tag `v1.2.1` (patch post-tag `v1.2.0`).

**Decisiones/acciones (pendientes que enmarcan la Fase 5):**
- Entregables del plan (docs/plan_implementacion.md §Fase 5):
  1. Definir, con el equipo, qué endpoints exigen qué roles (hoy solo `/roles/*` exige `ADMIN`).
  2. Agregar `Depends(require_roles(...))` según lo decidido.
  3. Test de autorización: 403 si el usuario no tiene el rol.
- Las 6 decisiones del equipo que bloquean el arranque:
  1. ¿`POST /usuarios/` público o requiere ADMIN? (hoy público)
  2. ¿Qué roles hay además de ADMIN y USUARIO?
  3. ¿`GET /usuarios/` y `GET /usuarios/{id}` requieren ser el mismo usuario o ADMIN?
  4. ¿`DELETE /usuarios/{id}` requiere ser ADMIN?
  5. ¿`POST /usuarios/{id}/roles` solo ADMIN? (hoy solo JWT)
  6. ¿Refresh token o solo access token?
- Recordatorio técnico ya anotado en `estado_actual_proyecto.md`: los roles viajan en el token JWT (stateless), por lo que asignar/quitar rol exige re-login para que se refleje en `/auth/me` y en la autorización.

**Archivos/módulos tocados:** ninguno de código en esta entrada (solo este documento y `docs/estado_actual_proyecto.md`). Rama `feature/autorizacion-roles` creada sin commits todavía.

**Estado resultante:** checklist en verde (unitarios 67/67, integración 5/5, `ruff`/`black` OK). `develop` = `c0aaba8` pusheado. Fase 5 en `feature/autorizacion-roles`, pendiente de definición de política de roles con el equipo; Fase 6 (cierre) queda después.

---

## 2026-09-14 — Fase 5 completada: autorización por rol con patrón híbrido (JWT corto + cache de estado)

**Qué se hizo:** se implementó la Fase 5 (autorización por rol) en `feature/autorizacion-roles`, siguiendo las decisiones del equipo (matriz completa, UC10 quitar rol, autoasignación de USUARIO en el alta, y patrón híbrido JWT corto + cache de estado con TTL para revocación en caliente).

**Decisiones/acciones:**
- **Patrón híbrido**: access token JWT de vida corta (default `JWT_EXPIRATION_MINUTES` 60 → 15) + cache de estado por `user_id` (activo + roles) con TTL 60s. Nuevo port `EstadoUsuarioCachePort` (obtener/guardar/invalidar) y modelo de dominio `EstadoUsuario`; adapter `EstadoUsuarioCacheMemoria` con `cachetools.TTLCache` (`cachetools==6.0.0` agregado a `app/requirements.txt`). Config: `AUTH_CACHE_TTL_SEGUNDOS=60`, `AUTH_CACHE_MAX_ITEMS=1000`.
- **`get_current_user` reescrito**: ya no confía en las claims del token; resuelve activo + roles desde cache (miss → BD vía `UsuarioQueryRepository.obtener_por_id` + `RolQueryRepository.obtener_nombres_por_ids`) y rechaza usuarios inactivos (401). Esto resuelve el pendiente histórico §7.5 y el stateless-bug §7.6 (revocación sin re-login).
- **Matriz de roles aplicada** a `/usuarios/*`: listar → `require_roles("ADMIN")`; obtener/actualizar → nueva dependencia `require_mismo_usuario_o_admin` (ADMIN o el propio `id`); baja, asignar y quitar rol → ADMIN. `POST /usuarios/` queda público. `/roles/*` sigue ADMIN.
- **UC2 autoasigna `USUARIO`**: el use case recibe `RolCommandPort`, resuelve el rol por nombre y `repo.crear` asocia los `RolORM` de `usuario.ids_roles`. Si el rol no existe, crea sin rol (no rompe el alta).
- **UC10 quitar rol**: nuevo `uc10_quitar_rol.py` + método `quitar_rol` en `UsuarioCommandPort` y su repositorio (remueve de `orm.roles`) + endpoint `DELETE /usuarios/{id}/roles/{rol_id}` con `require_roles("ADMIN")`.
- **Revocación en caliente**: UC6 (baja), UC9 (asignar) y UC10 (quitar) inyectan `EstadoUsuarioCachePort` e invalidan la entrada del usuario; el próximo request recarga desde BD. Verificado por integración sin re-login.
- **Bootstrap de admin en tests de integración**: como las operaciones de rol exigen ADMIN y la limpieza borra `usuarios`, el conftest crea/recrea `admin@bootstrap.com` (rol ADMIN) en cada test (hash con bcrypt vía `build_hasher`).
- `.env` local y `.env.example`: `JWT_EXPIRATION_MINUTES=15` + vars de cache.

**Archivos/módulos tocados:**
- Nuevos: `app/domain/models/estado_usuario.py`, `app/domain/ports/authentication/estado_usuario_cache_port.py`, `app/infrastructure/cache/` (`__init__.py`, `estado_usuario_cache_memoria.py`), `app/application/use_cases/uc10_quitar_rol.py`, `tests/unit/domian/services/test_uc10_quitar_rol.py`, `tests/integration/test_autorizacion_roles.py`.
- Modificados: `app/infrastructure/dependencies/auth_dependencies.py` (get_current_user híbrido + require_mismo_usuario_o_admin), `dependency_injection.py` (cache singleton, UC2/UC6/UC9 con nuevos deps, UC10), `app/presentation/routers/usuarios.py` (matriz + endpoint UC10), `app/application/use_cases/uc2_registrar_usuario.py`, `uc6_dar_de_baja_usuario.py`, `uc9_asignar_rol.py`, `app/domain/ports/usuario/usuario_command_port.py` (quitar_rol), `app/infrastructure/database/repositories/usuario_command_repository.py` (crear con roles + quitar_rol), `app/infrastructure/core/config.py`, `app/requirements.txt`, `tests/unit/domian/services/test_uc2_registrar_usuario.py`, `test_uc6_dar_de_baja_usuario.py`, `test_uc9_asignar_rol.py`, `tests/integration/conftest.py`, `tests/integration/test_flujo_completo.py`, `.env`, `.env.example`.
- Docs: `docs/estado_actual_proyecto.md`, `docs/plan_implementacion.md` (Fase 5 ✅ + decisiones resueltas).

**Estado resultante:** Fase 5 cerrada en `feature/autorizacion-roles` (sin commitear todavía). Checklist en verde: `pytest` 75 unitarios + 13 integración contra BD real, `ruff` y `black` OK. Pendiente: Fase 6 (cierre: merge a develop + tag semver).

---

## 2026-09-14 — Fase 6 completada: cierre documental (merge a develop, tag v1.3.0, limpieza de ramas)

**Qué se hizo:** se cerró la Fase 6 (cierre) de forma **documental** (decisión del usuario: no se tocó `main` ni se creó tag de cierre; microservicio completo y verificado en `develop`). Operaciones git previas al cierre: merge de `feature/autorizacion-roles` → `develop` (`84a93b6`, `--no-ff`, previa integración de `origin/develop`), tag anotado `v1.3.0`, push de `develop` (`c0aaba8..84a93b6`) y del tag, y limpieza de ramas ya mergeadas.

**Decisiones/acciones:**
- Cierre de fases del plan: los entregables de la Fase 6 (tag por fase, docs al día, tests en verde, merge a develop) ya estaban cubiertos; el tag de la última fase es `v1.3.0` (pusheado).
- **Release a `main`: queda pendiente y no bloquea** — `main` quedó atrasado respecto de `develop`. Se documentó como residual en `estado_actual_proyecto.md` §7.
- Se creó la rama `feature/fase-6-cierre` desde `develop` para el cierre (sin commits de código; solo contendrá el cierre documental). Queda disponible para reutilizar en un futuro release.
- **Limpieza de ramas**: se borraron las features ya mergeadas en `develop`, local y remoto: `feature/autorizacion-roles`, `feature/docs-readme`, `feature/migracion-bd`, `feature/tests-fase-3`, `feature/tests-integracion`. La excepción fue `origin/feature/docs-readme`, que el remoto **rechazó borrar por ser la rama default de GitHub** (refusing to delete the current branch); para limpiarla hay que cambiar el default branch en Settings → Branches.
- Punto de realidad post-cierre: ramas locales = `develop` (actualizada), `main`, `feature/fase-6-cierre`; remotas = `develop`, `main`, `feature/docs-readme`. Tags `v1.0.0`…`v1.3.0`.

**Archivos/módulos tocados:**
- `docs/plan_implementacion.md` — Fase 6 ✅ (entregables marcados + notas de cierre documental).
- `docs/estado_actual_proyecto.md` — §7 agregado pendiente nº7: release a `main` atrasado y nota de cierre documental de la Fase 6.
- Sin cambios de código.

**Estado resultante:** Fase 6 completada. Checklist en verde (`ruff`/`black`/`pytest` 75 unitarios + 13 integración contra BD real). `develop` = `84a93b6` pusheado, tag `v1.3.0` pusheado. Pendiente futuro (no bloqueante): release de `develop` → `main`.

---

## 2026-09-14 — Documentación completa por ingeniería inversa (formato Benn, uso educativo)

**Qué se hizo:** se generó la documentación integral del proyecto **por ingeniería inversa desde el
código ya implementado**, replicando el formato de `api_normalizacion_afiliados/docs/` (formato Benn
backend-only con carpetas numeradas `01_..06_` + HUs). Trabajo realizado en la rama
`feature/documentacion` (basada en `feature/fase-6-cierre`, que incluye el cierre documental de Fase 6).

**Decisiones/acciones (definidas con el usuario):**
- **Una HU por caso de uso** → `docs/04_historias_usuario/HU-01..HU-10` (5 archivos c/u: tarjeta,
  `_api.md`, `_caso_uso_expandido.md`, `_modelos_datos.md`, `_pruebas.md`).
- **Se usó `_pruebas.md`** (corregido), no el typo heredado `_pruevas.md` del repo de referencia.
- **Diagramas PlantUML `.puml` + `.svg`**: 7 diagramas (arquitectura, casos de uso, clases, objetos,
  ER, secuencia login UC1 y secuencia de autorización híbrida/revocación). El render se hizo con
  `plantuml.jar` descargado a `/tmp/opencode` usando el **motor Smetana** (`!pragma layout smetana`)
  porque la máquina no tiene Graphviz (`dot`). Los SVG quedaron con nombres snake_case
  (`arquitectura_diagrama.svg`, `secuencia_login.svg`, etc.).
- **Sin duplicados en la raíz** de `docs/` (a diferencia del repo de referencia, que duplica
  `decisiones_tecnicas.md` y `diagramas/`): en este repo quedaron `01_global/..06_auditorias/`,
  `02_tecnico/diagramas/` (canónico) y los 3 doc existentes en raíz (`estado_actual_proyecto.md`,
  `plan_implementacion.md`, `vitacora_agentica.md`).
- Se documentó la **HU-10 (quitar rol)** aunque no figuraba en AGENTS.md: el código ya la tiene
  (UC10, Fase 5); quedó anotado en la auditoría.
- `docs/02_tecnico/decisiones_tecnicas.md` describe el **patrón híbrido** (JWT corto + cache TTL,
  revocación en caliente) como decisión clave del diseño.

**Archivos/módulos tocados:** (solo `docs/`, sin código)
- Nuevos: `01_global/` (vision, alcance, actores, reglas_negocio), `02_tecnico/` (decisiones_tecnicas,
  modelo_datos_global + `diagramas/` con 7 `.puml` + 7 `.svg`), `03_procesos/definicion_listo.md`,
  `04_historias_usuario/HU-01..HU-10/` (50 md), `05_metodologia_agil/metodoKanban.md`,
  `06_auditorias/auditoria-historias-usuario.md`.
- Modificados: `docs/estado_actual_proyecto.md` (nueva §9 Documentación).

**Estado resultante:** proyecto totalmente documentado para uso educativo/explicativo. Checklist
en verde (`ruff`/`black`/`pytest` 75 unitarios + 13 integración). Commits atómicos por lote en
`feature/documentacion`. Pendiente: revisión del usuario y, si aprueba, integración a `develop`
(merge + tag, requiere OK explícito).

---

## 2026-09-17 — Sincronización de documentación: cambios del 15/09 no registrados + auditoría

**Qué se hizo:** se auditó el repositorio y se detectó que hubo cambios (2026-09-15) que no quedaron
registrados en la documentación (AGENTS.md, `docs/` y `README.md` quedaron desactualizados). Se
sincronizó la doc al estado real y se limpiaron hallazgos de la auditoría.

**Cambios reales que ya estaban hechos en git/BD y NO estaban documentados:**
- **Contenedorización (15/09, `7a8e646` + merges `1f22039`/`0022860`)**: se agregaron `Dockerfile`,
  `docker-entrypoint.sh` y `.dockerignore` para despliegue en contenedor.
- **README actualizado al estado real** (`f75351d`): fases completas, UC1..UC10, patrón híbrido.
- **Release a `main` ya realizado**: `0022860` (merge `develop` → `main`, Fase "contenedorización").
  `main` quedó **adelante** de `develop` (contiene todo + el merge). La nota "release a main pendiente"
  y la rama `feature/fase-6-cierre` quedaron obsoletas (la rama ya no existe).
- **Tag `v1.4.0`** (`4c9dedd`, 15/09 07:00): merge de `feature/documentacion` en `develop` (Fase 6).

**Hallazgos de la auditoría y resoluciones:**
- `AGENTS.md` desactualizado desde Fase 4: tabla de UCs, pendientes, UC10, patrón híbrido y comandos
  docker → actualizado al estado real.
- `docs/estado_actual_proyecto.md`: §6 (agregar contenedorización + `v1.4.0`), §7 (release ya hecho,
  `main` adelante, rama `feature/fase-6-cierre` inexistente) y fecha de última actualización.
- `docs/plan_implementacion.md`: Fase 6 (tag real `v1.4.0`, `main` mergeado) + contenedorización post-cierre.
- `README.md`: estado de Fase 6/release corregido, estructura + roadmap con Docker.
- `pyproject.toml`: se eliminó `per-file-ignore` fantasma de `app/infrastructure/google/google_sheets_client.py`
  (ruta inexistente heredada del scaffold de `api_normalizacion_afiliados`).
- **Rama default de GitHub**: se cambió de `feature/docs-readme` a `main` vía `gh` (con OK explícito del usuario).

**Archivos/módulos tocados:** `AGENTS.md`, `README.md`, `docs/vitacora_agentica.md`,
`docs/estado_actual_proyecto.md`, `docs/plan_implementacion.md`, `pyproject.toml`.

**Estado resultante:** documentación sincronizada al estado real (git + BD). Checklist en verde
(`ruff`/`black`/`pytest`) tras la verificación. Sin cambios de código funcional. Sin tags nuevos
(decisión del usuario: "dejar como está").

---
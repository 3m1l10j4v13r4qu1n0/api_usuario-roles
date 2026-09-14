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
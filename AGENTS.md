# AGENTS.md

API REST de autenticación y autorización (usuarios + roles + JWT) en Python/FastAPI con Clean Architecture + Hexagonal (Ports & Adapters). Responder siempre en español (latino).

## Idioma y tono

- Responder siempre en español rioplatense, informal ("vos"). Nunca en inglés,
  aunque el código, logs o skills estén en inglés.

## Comandos

- Todo se ejecuta **desde la raíz del repo** (los imports son `app.*`), no desde `app/`.
- Levantar API: `uvicorn app.main:app --reload`
- Migraciones (Alembic ya está inicializado, **no** hacer `alembic init`):
  - `alembic revision --autogenerate -m "descripcion"`
  - `alembic upgrade head`
- Tests unitarios (puros, sin BD): `pytest` desde la raíz. Sanity check: `python -m pytest tests/unit/domian/services -q`
- Seed de datos iniciales (roles ADMIN y USUARIO): `python -m app.infrastructure.database.seed_runner`
- Lint y formato antes de cada commit:
  - `venv/bin/ruff check .`
  - `venv/bin/black --check .`
  - `venv/bin/python -m pytest -q`

## Setup / gotchas

- `requirements.txt` está en **`app/requirements.txt`** (no en la raíz).
- Python fijado a **3.13.5** (`app/.python-version`). No hay venv commitado.
- Config lee variables de entorno via pydantic-settings desde `.env` (ver `app/infrastructure/core/config.py`). Var obligatoria: `DATABASE_URL` (PostgreSQL async, `postgresql+asyncpg://...`).
- **Variables JWT**: `JWT_SECRET_KEY` (obligatoria), `JWT_ALGORITHM` (HS256) y `JWT_EXPIRATION_MINUTES` (60) — ver `.env.example`.
- **`bcrypt` y `PyJWT`** están listados en `app/requirements.txt` (hashing de contraseñas y emisión/validación de tokens). Nunca se usan dentro de `app/domain/`; los adapters viven en `app/infrastructure/auth/`.
- La base usa SQLAlchemy 2.0 async (`AsyncSession`, `asyncpg`). `get_db()` en `connection.py` hace **commit automático al finalizar el request** — los casos de uso no deben commitear.
- Un usuario se da de baja con **baja lógica** (`activo = False`); el login rechaza usuarios inactivos.
- Test de login usa fakes; el directorio de tests unitarios de dominio es `tests/unit/domian/` (tipeo original heredado).

## Arquitectura

Capas (regla: el dominio no importa frameworks, ni siquiera `bcrypt`/`PyJWT`):

- `app/domain/` — entidades puras (`models/usuario.py`, `models/rol.py`), servicios (`services/validacion.py`, `normalizacion.py`, `auth_service.py`) y **ports** (contratos `ABC` + `abstractmethod`). `exceptions.py` define excepciones de dominio (`DatoInvalidoError`, `EmailDuplicadoError`, `CredencialesInvalidasError`, `NoAutorizadoError`, `TokenInvalidoError`, `UsuarioNoEncontradoError`, `RolNoEncontradoError`).
- `app/application/use_cases/` — casos de uso `ucN_*.py` (clases `...UseCase` con `async def execute`), reciben ports, no implementaciones concretas.
- `app/infrastructure/` — adapters: ORM + repositorios en `database/`, hashing/tokens en `auth/` (`password_hasher.py` con bcrypt, `jwt_token_provider.py` con PyJWT), y el wiring en `dependencies/` (`dependency_injection.py` + `auth_dependencies.py` con `get_current_user` y `require_roles`).
- `app/presentation/` — routers FastAPI (`auth.py`, `usuarios.py`, `roles.py`), schemas Pydantic y `handlers.py` para traducir excepciones de dominio a HTTP (payload `{"error": str(exc)}`).

Convenciones:

- Todo caso de uso nuevo debe cablearse en `dependency_injection.py` (función `get_*` con `Depends(get_db)`) e inyectarse en el router con `Depends`.
- Endpoints protegidos inyectan `get_current_user` (JWT). Autorización por rol: `Depends(require_roles("ADMIN"))`.
- Excepciones de dominio se mapean a HTTP solo en `handlers.py`; no usar `try/except` de negocio en routers/use cases.
- Tests unitarios usan `Fake*`/in-memory para aislar el dominio, sin BD.
- Reglas SOLID aplicadas al escribir código Python: ver `.agents/rules/reglas-solid.md`.

## Flujo de implementación (reglas duras)

### Al recibir una tarea

1. **Leer `docs/estado_actual_proyecto.md`** completo antes de tocar código.
2. **Verificar** que la funcionalidad no exista ya (leer código relevante, no asumir).
3. **Planificar** en pasos chicos (un caso de uso, un endpoint, o un componente por vez).
4. **Preguntar** ante ambigüedad; no decidir por cuenta propia.

### Al escribir código

- **Un archivo = una responsabilidad** (SRP). No mezclar persistencia, dominio y transporte.
- **Ports chicos y específicos**: preferir varios puertos pequeños antes de uno gordo con métodos que nadie usa.
- **Dominio puro**: `app/domain/` NO importa FastAPI, SQLAlchemy, Pydantic, `bcrypt` ni `PyJWT`.
- **Inyección de dependencias**: cablear en `dependency_injection.py` con `Depends`, nunca instanciar adapters dentro de casos de uso.
- **Releer después de escribir**: verificar que el archivo quedó como se planeó.
- **Trabajo en pasos chicos**: mostrar qué se hizo y qué falta antes de seguir.

### Al commitear

- **Conventional Commits en español**, scope en minúscula:
  - `feat(domain): se agrega puerto PasswordHasherPort`
  - `fix(usecase): se corrige validacion de password en login`
  - `test(usecase): se agrega test de UC1`
- **Un tema por commit** (commits atómicos). Si necesita "y", son dos commits.
- **Prohibido** mensajes vagos ("cambios", "update", "cosas varias").
- **Checklist** antes de commit:
  ```bash
  venv/bin/ruff check .
  venv/bin/black --check .
  venv/bin/python -m pytest -q
  ```

### Flujo de ramas y merges (regla dura: `.agents/rules/flujo-git.md`)

- **Prohibido** trabajar directo sobre `main` o `develop`.
- Crear `feature/<tema>` o `fix/<tema>` **siempre desde `develop`**.
- Una rama = una tarea/HU coherente. Mantener ramas cortas.
- **Antes de mergear a develop**:
  1. Integrar `origin/develop` dentro de la rama feature (`git fetch` + `git merge origin/develop`) y resolver conflictos ahí.
  2. Checklist en verde: `ruff check` · `black --check` · `pytest`.
  3. Solo entonces mergear a develop.
- **Push/merge SOLO con aprobación explícita del usuario**.

### Versionado por fases (regla dura: `.agents/rules/versionado-fases.md`)

- **Tag anotado** al cerrar cada fase, **no** push por ahora.
- Versión semver: cada fase incrementa la versión menor (`v1.0.0` → `v1.1.0` → `v1.2.0`).
- **Nunca** push de rama o tag sin aprobación explícita del usuario.
- Si una fase se corrige después del tag, versionar con patch (`vX.Y.Z+1`).

## Reglas de verificación y anti-alucinación (`.agents/rules/Reglas-anti-alucinacion.md`)

- **Verificar antes de afirmar**: leer el archivo/símbolo en la sesión actual, no asumir de memoria.
- **No inventar superficie de código**: nombres de clases, métodos, rutas, endpoints — solo si se vieron en código real o se marcan como "nuevo, a crear".
- **No inventar dependencias**: solo citar librerías verificadas en `requirements.txt`.
- **Ambigüedad → pregunta**: no decidir por cuenta propia.
- **Confirmación explícita en cambios transversales**: cambios que toquen más de una HU requieren OK del usuario.
- **Reporte de cada paso**: 1) qué se verificó, 2) qué se propone/cambió, 3) qué queda pendiente.

## Fuente de verdad

- `docs/` es la única fuente de verdad para requerimientos, especificaciones y reglas de negocio.
- No inventar endpoints, campos, tipos, textos ni contenido institucional.
- Si el código real contradice `docs/estado_actual_proyecto.md`, avisar antes de asumir cuál es la fuente.

## Notas

- `docs/plan_implementacion.md` define el plan por fases (andamiaje → base → autenticación → autorización → cierre).
- El skill `di-architect-scaffold` en `.agents/skills/` define el flujo de 6 pasos para implementar casos de uso/HUs en este proyecto (ya adaptado de `api_normalizacion_afiliados`).
- El skill `rest-api-design` tiene una guía local adaptada: `.agents/skills/rest-api-design/references/fastapi-conventions.md` + template `templates/endpoint_fastapi.py` (mapeo de status codes por excepción de dominio, naming vigente, convenciones REST para endpoints nuevos).
- Roles por defecto creados por seed: `ADMIN`, `USUARIO`.
- Endpoints públicos hoy: `POST /auth/login`, `POST /usuarios/`, `GET /`. El resto requiere token JWT; `/roles/*` además requiere rol `ADMIN`.

## Casos de uso — Estado verificado

| UC | Descripción | Estado | Notas |
|---|---|---|---|
| UC1 | Login con JWT | 🟡 parcial | Case de uso + endpoint `POST /auth/login` + `GET /auth/me` implementados; falta migración de esquema y prueba contra BD real |
| UC2 | Registrar usuario | 🟡 parcial | Case de uso + endpoint implementados; sin migración / BD |
| UC3 | Listar usuarios | 🟡 parcial | Implementado; protegido con JWT |
| UC4 | Obtener usuario por ID | 🟡 parcial | Implementado; protegido con JWT |
| UC5 | Actualizar usuario | 🟡 parcial | Implementado; protegido con JWT |
| UC6 | Dar de baja usuario (baja lógica) | 🟡 parcial | Implementado; protegido con JWT |
| UC7 | Crear rol | 🟡 parcial | Implementado; requiere rol ADMIN |
| UC8 | Listar roles | 🟡 parcial | Implementado; requiere rol ADMIN |
| UC9 | Asignar rol a usuario | 🟡 parcial | Implementado; protegido con JWT |

Leyenda: ✅ verificado en sesión | 🟡 parcial | 🔵 pendiente externo/no implementado | ⏳ en proceso

## Pendientes de implementación

- Crear la migración inicial de Alembic (`alembic revision --autogenerate`) para las tablas `usuarios`, `roles` y `usuario_roles`.
- Correr `alembic upgrade head` y el seed contra una BD PostgreSQL real.
- Escribir tests de los UCs restantes (UC2..UC9) con fakes.
- Revisar autorización por rol: hoy `/roles/*` exige `ADMIN`; decidir con el equipo qué roles aplican al resto de endpoints.
- Decidir si `POST /usuarios/` debe ser público o exigir rol ADMIN (hoy es público para permitir el alta inicial).

## Memoria del proyecto (docs/estado_actual_proyecto.md y docs/vitacora_agentica.md)

- Antes de tocar código, leer `docs/estado_actual_proyecto.md` completo para tener el contexto actual del proyecto.
- Al terminar una implementación, eliminación o edición relevante (nueva entidad, caso de uso, endpoint, refactor de arquitectura, dependencia core):
  1. Actualizar la sección correspondiente de `docs/estado_actual_proyecto.md` (editar in-place, no reescribir todo el archivo).
  2. Agregar una entrada nueva al final de `docs/vitacora_agentica.md` con: fecha, qué se hizo, decisiones tomadas, archivos tocados y estado resultante. Nunca editar entradas previas de la vitácora.
- No generar entradas de vitácora por cambios triviales (typos, formateo, renames cosméticos).
- Si el código real contradice lo que dice `estado_actual_proyecto.md`, avisar antes de asumir cuál es la fuente de verdad.
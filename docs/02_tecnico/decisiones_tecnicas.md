# Decisiones Técnicas — API de Usuarios y Roles

## 1. Stack tecnológico

| Capa | Tecnología | Versión | Motivo |
|---|---|---|---|
| Lenguaje | Python | 3.13.5 (`app/.python-version`) | Tipado moderno (dataclasses, `Mapped`, union types) |
| Framework web | FastAPI | 0.135.1 | Async nativo, Pydantic v2, autodoc OpenAPI |
| ORM | SQLAlchemy 2.0 async | 2.0.48 | `AsyncSession` + `asyncpg`; estilo `Mapped`/`mapped_column` |
| Driver BD | asyncpg | 0.31.0 | Conexión async a PostgreSQL |
| Migraciones | Alembic | 1.18.4 | `env.py` async, `target_metadata = Base.metadata` |
| Validación | pydantic-settings | 2.13.1 | Config por `.env` |
| Hashing | bcrypt | 4.3.0 | Hash seguro de contraseñas |
| Tokens | PyJWT | 2.10.1 | Emisión/validación HS256 |
| Cache | cachetools | 6.0.0 | `TTLCache` de estado de sesión |
| Email validation | email-validator | 2.3.0 | `validate_email` en dominio |
| Tests | pytest + httpx | — | `TestClient` contra BD real en integración |
| Lint/format | ruff + black | — | `pyproject.toml` (line-length 100) |

## 2. Autenticación y autorización

- **Autenticación**: `POST /auth/login` valida credenciales (bcrypt) y emite un token JWT corto
  por defecto (15 min, `JWT_EXPIRATION_MINUTES`). Payload: `sub` (id), `roles`, `iat`, `exp`.
- **Autorización por rol**: siempre **intersección** (`autorizar`), el usuario debe poseer
  *alguno* de los roles requeridos. Dependencias:
  - `require_roles("ADMIN")` — endpoints exclusivos de ADMIN.
  - `require_mismo_usuario_o_admin` — ADMIN **o** el propio usuario (ownership).
- **Patrón híbrido (clave del diseño)**:
  - El JWT solo aporta **identidad**. La autorización **no confía en las claims del token**:
    `get_current_user` resuelve el estado real (`activo` + roles) desde un cache por TTL corto
    (`TTLCache`, 60 s por defecto) y, en miss, lo carga de la BD y lo cachea.
  - **Revocación en caliente**: UC6 (baja), UC9 (asignar rol) y UC10 (quitar rol) invalidan el
    cache del usuario; el cambio se refleja en el próximo request **sin re-login**.
  - Si el servicio se escala horizontalmente, el cache in-memory debe reemplazarse por uno
    compartido (Redis); el port `EstadoUsuarioCachePort` soporta el swap sin tocar el dominio.

## 3. Arquitectura

Clean Architecture + Hexagonal (Ports & Adapters). Capas y regla de dependencia:

| Capa | Responsabilidad | Importa frameworks |
|---|---|---|
| `domain` (Core) | Entidades `Usuario`, `Rol`, `EstadoUsuario`; servicios `normalizacion`, `validacion`, `auth_service`; **ports** (contratos ABC); excepciones | **Nunca** (ni fastapi, sqlalchemy, bcrypt ni PyJWT) |
| `application` | Casos de uso `ucN_*.py`, cada uno con `async def execute`; inyectan ports | Solo dominio |
| `infrastructure` | Adapters: ORM/repositorios, bcrypt, PyJWT, cache, wiring (`dependency_injection`, `auth_dependencies`) | FastAPI (para `Depends`), SQLAlchemy, etc. |
| `presentation` | Routers, schemas Pydantic, `handlers` (excepción dominio → HTTP) | FastAPI, Pydantic |

Flujo: `router → dependency_injection → use case → ports → adapters → BD/BCrypt/PyJWT/cache`.

## 4. Estructura de carpetas

```
app/
├── domain/                      # Core puro (sin frameworks)
│   ├── models/                  # usuario.py · rol.py · estado_usuario.py
│   ├── services/                # normalizacion.py · validacion.py · auth_service.py
│   ├── ports/                   # authentication/ · usuario/ · rol/  (ABC)
│   └── exceptions.py
├── application/use_cases/       # uc1_login.py … uc10_quitar_rol.py
├── infrastructure/
│   ├── core/                    # config.py (Settings) · connection.py (AsyncSessionLocal, get_db)
│   ├── database/                # orm_models/ (UsuarioORM, RolORM, usuario_roles) · repositories/ · seed.py · seed_runner.py
│   ├── auth/                    # password_hasher.py (bcrypt) · jwt_token_provider.py (PyJWT)
│   ├── cache/                   # estado_usuario_cache_memoria.py (cachetools TTLCache)
│   └── dependencies/            # dependency_injection.py · auth_dependencies.py
├── presentation/
│   ├── routers/                 # auth.py · usuarios.py · roles.py
│   ├── schemas/                 # auth_schema.py · usuario_schema.py · rol_schema.py
│   └── handlers.py              # excepción de dominio → HTTP ({"error": ...})
└── main.py                      # lifespan, CORS, handlers, routers, GET /
alembic/                         # env.py (async) + versions/9378f376749f_crear_tablas_usuarios_roles.py
tests/
├── unit/domian/services/        # tests puros con fakes (typo heredado "domian")
└── integration/                 # BD real + TestClient (conftest con bootstrap admin)
```

## 5. Variables de entorno

Viven en `.env` (no commiteado); plantilla en `.env.example`. Leídas por `Settings` (pydantic-settings).

| Variable | Obligatoria | Default | Descripción |
|---|---|---|---|
| `DATABASE_URL` | ✅ | — | PostgreSQL async (`postgresql+asyncpg://...`) |
| `JWT_SECRET_KEY` | ✅ | — | Clave secreta para firmar HS256 |
| `APP_NAME` / `APP_VERSION` | — | API Usuarios y Roles / 1.0.0 | Nombre y versión |
| `DEBUG` | — | `False` | Modo debug (bcrypt rounds bajos, echo SQL) |
| `JWT_ALGORITHM` | — | `HS256` | Algoritmo JWT |
| `JWT_EXPIRATION_MINUTES` | — | `15` | Expiración del access token |
| `AUTH_CACHE_TTL_SEGUNDOS` | — | `60` | TTL del cache de estado |
| `AUTH_CACHE_MAX_ITEMS` | — | `1000` | Máx. entradas del cache |
| `CORS_ORIGINS` | — | localhost:5173/3000 | Orígenes CORS |

## 6. Dependencias

Listadas en `app/requirements.txt` (no en la raíz). Detalle en §1. `email-validator` se usa en
dominio (`validacion.py`); `httpx` en los tests de integración (TestClient).

## 7. Decisión notable: `get_db()` con commit automático

`get_db()` crea la `AsyncSession`, hace yield al router y **commitea al finalizar el request**
(rollback en error). Por eso los casos de uso **no commitean**: el commit es transversal.

## 8. Decisión notable: manejo de datos

- `.env` no se commitea (`.gitignore`); seed idempotente (`seed_runner.py`);
  migración única `9378f376749f_crear_tablas_usuarios_roles` (tablas `usuarios`, `roles`,
  `usuario_roles`).
- Tests unitarios forzan `DATABASE_URL` por defecto en `tests/conftest.py` para no depender de `.env`.
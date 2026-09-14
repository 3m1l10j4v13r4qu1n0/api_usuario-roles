---
name: di-architect-scaffold
description: Estandarizar la implementación de la Inyección de Dependencias (DI) y el flujo de trabajo en proyectos basados en Clean Architecture + Hexagonal Architecture (Ports & Adapters), garantizando bajo acoplamiento, alta cohesión y facilitando las pruebas unitarias. Usar cuando el usuario pida implementar un nuevo caso de uso, repositorio, puerto, adapter o endpoint en el backend de la API de Usuarios y Roles.
disable-model-invocation: true
---

# DI Architect Scaffold — API Usuarios y Roles

Skill para scaffoldear módulos de la **API de Usuarios y Roles** (autenticación y
autorización JWT), que sigue Clean Architecture + Hexagonal Architecture
(Ports & Adapters). Los casos de uso del proyecto se denominan genéricamente **UC**
(ej. `UC1`, `UC2`) y el plan de implementación vive en `docs/plan_implementacion.md`.

## Stack tecnológico obligatorio

- Lenguaje: **Python 3.13.5** (ver `app/.python-version`)
- Framework Web: FastAPI
- Validación de datos: Pydantic V2
- ORM: SQLAlchemy 2.0 (asíncrono vía `AsyncSession` + `asyncpg`)
- Migraciones: Alembic (ya inicializado — **no** hacer `alembic init`)
- Base de datos: PostgreSQL
- Hashing de contraseñas & tokens: `bcrypt` y `PyJWT` (ver `app/requirements.txt`)
- Testing: Pytest (tests de dominio puros, sin BD)
- Linter/formatter: `ruff` y `black` (ver comandos en `AGENTS.md`)

## 📜 Reglas Inquebrantables del Proyecto

1. **Aislamiento del Dominio**: `app/domain/` NO puede importar nada de FastAPI,
   SQLAlchemy, Pydantic, `bcrypt` ni `PyJWT`. Solo Python puro.
2. **Inversión de Dependencias (DIP)**: los **ports** definen los contratos en
   `app/domain/ports/`. La infraestructura los implementa. Los casos de uso solo
   conocen los ports, nunca las implementaciones concretas.
3. **Manejo Centralizado de Excepciones**: prohibido usar `try/except` de negocio en
   Routers o Casos de Uso. Las excepciones de dominio se traducen a HTTP
   **exclusivamente** en `app/presentation/handlers.py`.
4. **Ciclo de Vida de Dependencias**: repositorios y casos de uso son *transient*
   (por request) cableados en `app/infrastructure/dependencies/dependency_injection.py`.
   El commit de la sesión de BD lo hace `get_db()` automáticamente — **no commitear
   dentro de los casos de uso**.
5. **Estructura de Carpetas Estricta**: respetar las capas
   `domain → application → infrastructure → presentation`.

## 📌 Reglas de negocio críticas (NO ignorar)

1. La validación de datos (email, password, nombre de usuario) vive en
   `app/domain/services/validacion.py` y lanza `DatoInvalidoError`. No duplicar esa lógica.
2. El **email es único** — los repositorios y casos de uso deben rechazar duplicados
   con `EmailDuplicadoError` (409 en HTTP).
3. **Hashing de contraseñas**: nunca se almacena texto plano; el hash se calcula vía el
   port `PasswordHasherPort` (implementado con `bcrypt` en `app/infrastructure/auth/`).
4. **Tokens JWT**: la emisión/validación va detrás del port `TokenProviderPort`
   (implementado con `PyJWT` en `app/infrastructure/auth/`). El dominio nunca toca el token crudo.
5. **Baja de usuario**: no se borra físicamente; se marca `activo = False`
   (baja lógica). El login rechaza usuarios inactivos.
6. Las excepciones heredan de `Exception`:
   `DatoInvalidoError`, `EmailDuplicadoError`, `UsuarioNoEncontradoError`,
   `CredencialesInvalidasError`, `NoAutorizadoError`, `TokenInvalidoError`,
   `RolNoEncontradoError`.

## 🔄 Flujo de trabajo estándar (6 pasos)

Cada vez que se solicite implementar un nuevo Caso de Uso (UC) o módulo, seguir este
orden y **esperar confirmación explícita ("Continuar") antes de avanzar al siguiente paso**.

### Paso 1: Definición de Contratos y Excepciones (Dominio)
**Ubicación**: `app/domain/`
1. Definir/actualizar la entidad pura en `app/domain/models/`.
2. Definir las excepciones de dominio en `app/domain/exceptions.py` (herencia directa de `Exception`).
3. Definir el **port**/contrato en `app/domain/ports/` usando `ABC` + `abstractmethod`
   (patrón real del repo), con docstring citando el `UC` que cubre
   (ver `app/domain/ports/usuario/usuario_query_port.py`).

### Paso 2: Implementación de Adaptadores Concretos (Infraestructura)
**Ubicación**: `app/infrastructure/`
1. Crear el modelo ORM de SQLAlchemy en `database/orm_models/` (debe heredar de
   `Base` de `connection.py`).
2. Crear el repositorio en `database/repositories/` que implemente el `ABC` del Paso 1.
3. Si el port es de auth (hash/token), crear el adapter en `auth/`.
4. El repositorio debe lanzar **excepciones de dominio** (no de SQLAlchemy) cuando se
   violen reglas de negocio (ej. duplicados).

### Paso 3: Configuración del Wiring (Inyección de Dependencias)
**Ubicación**: `app/infrastructure/dependencies/dependency_injection.py`
1. Crear una función "getter" (fábrica) que devuelva la instancia del Caso de Uso.
2. La función instancia el Repositorio Concreto (con `session: AsyncSession = Depends(get_db)`)
   y lo inyecta en el Caso de Uso, usando `Depends`.
3. Los ports de auth (hasher/token) se instancian una sola vez (singleton) y se reutilizan.
4. Registrar el getter en el router con `Depends`.

### Paso 4: Lógica de Negocio (Capa de Aplicación)
**Ubicación**: `app/application/use_cases/`
1. Crear la clase del Caso de Uso con **nombre de archivo `ucN_descripcion.py`** y clase
   `NombreUseCase` (ej. `uc2_registrar_usuario.py` → `RegistrarUsuarioUseCase`).
2. El `__init__` recibe **únicamente** los ports, nunca implementaciones concretas
   (`self._repo = repo`).
3. El método `async def execute(...)` orquesta la lógica, llama al port y deja que las
   excepciones de dominio burbujeen (incluir docstring citando `UC`).

### Paso 5: Exposición y Manejo de Errores (Capa de Presentación)
**Ubicación**: `app/presentation/`
1. Definir DTOs de entrada/salida con Pydantic en `schemas/`.
2. Definir el endpoint en `routers/` (`auth.py` para login/me, `usuarios.py` para el CRUD),
   inyectando el Caso de Uso con `Depends(get_*_ucN)`.
3. **Regla crítica**: en `handlers.py`, registrar `@app.exception_handler(TuExcepcionDeDominio)`
   mapeando cada excepción a su código HTTP con payload `{"error": str(exc)}`.

### Paso 6: Pruebas de Aislamiento (Testing)
**Ubicación**: `tests/unit/domian/services/` (el directorio se llama `domian`, tipeo heredado)
1. Crear un `FakeRepository`/implementación en memoria que cumpla el contrato del dominio.
2. Inyectar el fake en el Caso de Uso.
3. Escribir tests que verifiquen comportamiento exitoso y que se lancen las excepciones
   de dominio correctas ante datos inválidos, sin tocar la BD real.
4. Correr desde la raíz del repo: `venv/bin/python -m pytest tests/unit/domian/services -q`

## 📋 Esquema de capas (a seguir al agregar un módulo)

```text
app/
├── domain/
│   ├── models/x.py                       # Entidad pura (sin frameworks)
│   ├── ports/.../ix_port.py              # ABC + abstractmethod
│   └── exceptions.py                     # Excepciones de dominio (heredan de Exception)
├── application/
│   └── use_cases/ucN_accion_x.py         # Clase NAccionUseCase; __init__ recibe ports
├── infrastructure/
│   ├── database/orm_models/x_orm.py      # Modelo SQLAlchemy (hereda de Base)
│   ├── database/repositories/x_repository.py  # Implementa el port
│   ├── auth/x_adapter.py                 # Implementa PasswordHasherPort/TokenProviderPort
│   └── dependencies/dependency_injection.py   # get_*_ucN() con Depends(get_db)
└── presentation/
    ├── schemas/x_schema.py               # DTOs Pydantic
    ├── routers/auth.py o usuarios.py     # Endpoint con Depends(get_*_ucN)
    └── handlers.py                       # @app.exception_handler(...)
```

## 🌱 Cultura de Desarrollo de Software

Mantener código limpio, mantenible y con hábitos profesionales.

### Principios
- **Clean Code**: nombres descriptivos, una responsabilidad por función, legibilidad.
- **SOLID**: SRP, Open/Closed, Liskov, Interface Segregation, Dependency Inversion.
- **KISS / DRY / YAGNI**: solución más simple, sin duplicar lógica (reutilizar
  `validacion.py`, `normalizacion.py` del dominio).

### Estrategia de ramas
Prohibido trabajar directamente sobre `main` o `develop`.
(`develop` → `feature/...`, `fix/...`, `docs/...`, `test/...`.)

### Convención de commits
**Conventional Commits en español**, scope en minúscula: `feat(domain): ...`, `fix(usecase): ...`,
`docs(rules): ...`, `test(domain): ...`. Un tema por commit.

### Calidad del código
Antes de commitear: `venv/bin/ruff check .`, `venv/bin/black --check .` y
`venv/bin/python -m pytest -q` (desde la raíz). No subir código que no compile,
rompa tests, tenga código comentado innecesario o imports sin usar.

### Prohibido
- Trabajar sobre `main` o `develop`.
- Commits vagos ("cambios", "arreglos", "update").
- Duplicar lógica de negocio (reutilizar los servicios de dominio existentes).
- Acoplar el dominio con FastAPI, SQLAlchemy, Pydantic, `bcrypt` o `PyJWT`.
- `try/except` de negocio en routers/use cases.
- Clases o funciones excesivamente grandes.

## 🎯 Objetivo

Construir software mantenible, desacoplado y testeable aplicando Clean Architecture,
Hexagonal Architecture, SOLID y buenas prácticas, alineado al estilo ya establecido en
`app/application/use_cases/` y `app/infrastructure/dependencies/dependency_injection.py`.
# API Usuario-Roles

🔐 API REST de autenticación y autorización (usuarios + roles + JWT)  
⚡ FastAPI  
🏗️ Clean Architecture + Hexagonal (Ports & Adapters)  
🐍 Python 3.13.5  
🗄️ PostgreSQL async (SQLAlchemy 2.0 + asyncpg)

---

## 📌 Descripción general

Este proyecto implementa una API REST de **autenticación y autorización** que provee la capa de auth para un ecosistema mayor de microservicios (Frontend → API REST → servicios), gestionando usuarios, roles y la emisión/validación de tokens JWT.

El proyecto está diseñado como ejercicio práctico de **análisis funcional + desarrollo backend**, simulando un sistema real de gestión de accesos.

El sistema actúa como puerta de entrada a recursos protegidos, garantizando que solo usuarios autenticados (y autorizados por rol) accedan a los endpoints correspondientes.

**El alcance del proyecto se limita a la autenticación, gestión de usuarios y roles, y la autorización por rol, sin reemplazar a un sistema completo de gestión de identidades.**

---

## 🎯 Objetivos del proyecto

- Autenticar usuarios mediante JWT
- Gestionar usuarios (alta, consulta, actualización y baja lógica)
- Gestionar roles del sistema
- Asignar y quitar roles a usuarios
- Autorizar endpoints por rol
- Mantener el dominio desacoplado de frameworks (arquitectura limpia)

---

## 📚 Documentación

La documentación del proyecto se encuentra en `docs/`, separada por áreas:

- `estado_actual_proyecto.md` — foto actual del proyecto (fuente de verdad)
- `plan_implementacion.md` — plan por fases (andamiaje → base → autenticación → autorización → cierre)
- `vitacora_agentica.md` — historial cronológico append-only de decisiones
- `01_global/` — visión, alcance, actores y reglas de negocio (RN01..RN06 + USR-RN07..RN15)
- `02_tecnico/` — decisiones técnicas, modelo de datos global y **diagramas PlantUML** (`.puml` + `.svg` renderizados): arquitectura, casos de uso, clases, objetos, ER y secuencias (login UC1 + autorización híbrida)
- `03_procesos/` — Definition of Ready (DoR) y checklist de "listo para merge"
- `04_historias_usuario/HU-01..HU-10/` — una HU por caso de uso, con tarjeta, API, caso de uso expandido, modelos de datos y plan de pruebas
- `05_metodologia_agil/` — metodología Kanban con ciclo de desarrollo con IA
- `06_auditorias/` — auditoría de las 10 HUs vs código real

---

## ⚙️ Funcionalidades principales

- Login con emisión de token JWT (`sub` = id de usuario + `roles`)
- Registro de usuarios con contraseña hasheada (bcrypt)
- Listado y consulta de usuarios por ID
- Actualización parcial de usuarios (solo campos presentes, password rehasheada)
- Baja lógica de usuarios (`activo = False`)
- Creación y listado de roles
- Asignación y quita de roles a usuarios (tabla `usuario_roles`)
- **Patrón híbrido JWT + cache TTL**: token corto (15 min) + cache de estado (60 s) con revocación de rol/baja en caliente (sin esperar la expiración del JWT)
- Protección de endpoints por JWT y autorización por rol (`require_roles("ADMIN")`)
- Seed de roles iniciales (`ADMIN`, `USUARIO`)

---

## 🔌 Endpoints

| Método | Ruta | Descripción | Protección |
|---|---|---|---|
| GET | `/` | Health check | pública |
| POST | `/auth/login` | Autentica y devuelve token JWT (UC1) | pública |
| GET | `/auth/me` | Usuario autenticado desde el token | JWT |
| POST | `/usuarios/` | Registrar usuario (UC2) | pública* |
| GET | `/usuarios/` | Listar usuarios (UC3) | JWT + ADMIN |
| GET | `/usuarios/{usuario_id}` | Obtener usuario por ID (UC4) | JWT (ADMIN o propio) |
| PATCH | `/usuarios/{usuario_id}` | Actualizar usuario (UC5) | JWT (ADMIN o propio) |
| DELETE | `/usuarios/{usuario_id}` | Baja lógica (UC6) | JWT + ADMIN |
| POST | `/usuarios/{usuario_id}/roles` | Asignar rol a usuario (UC9) | JWT + ADMIN |
| DELETE | `/usuarios/{usuario_id}/roles/{rol_id}` | Quitar rol a usuario (UC10) | JWT + ADMIN |
| POST | `/roles/` | Crear rol (UC7) | JWT + ADMIN |
| GET | `/roles/` | Listar roles (UC8) | JWT + ADMIN |

> *`POST /usuarios/` queda **público** por decisión del equipo (revisitable) para permitir el alta inicial; autoasigna el rol `USUARIO`.
>
> Las respuestas de error usan payload uniforme `{"error": "mensaje"}`. Mapeo: 401 (credenciales/token inválido), 403 (rol no autorizado), 404 (no encontrado), 409 (email duplicado), 422 (datos inválidos).

---

## ✅ Casos de uso

| UC | Descripción | Estado |
|---|---|---|
| UC1 | Login con JWT (+ `GET /auth/me`) | ✅ completado |
| UC2 | Registrar usuario | ✅ completado |
| UC3 | Listar usuarios | ✅ completado |
| UC4 | Obtener usuario por ID | ✅ completado |
| UC5 | Actualizar usuario | ✅ completado |
| UC6 | Dar de baja usuario (baja lógica) | ✅ completado |
| UC7 | Crear rol | ✅ completado |
| UC8 | Listar roles | ✅ completado |
| UC9 | Asignar rol a usuario | ✅ completado |
| UC10 | Quitar rol a usuario | ✅ completado |

---

## 🏗️ Estructura del Proyecto

```
api_usuario-roles/
│
├── alembic/
│   ├── versions/
│   │   └── 9378f376749f_crear_tablas_usuarios_roles.py
│   ├── env.py
│   └── script.py.mako
│   💬 Migraciones de base de datos (esquema versionado)
│
├── app/
│
│   ├── main.py
│   💬 Punto de entrada de la aplicación (FastAPI)
│
│   ├── presentation/  🟦 CAPA DE PRESENTACIÓN (Delivery)
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── usuarios.py
│   │   │   └── roles.py
│   │   │   💬 Define endpoints REST (HTTP → Use Cases)
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth_schema.py
│   │   │   ├── usuario_schema.py
│   │   │   └── rol_schema.py
│   │   │   💬 DTOs de entrada/salida (Pydantic)
│   │   │
│   │   └── handlers.py
│   │       💬 Traduce excepciones de dominio → HTTP (payload {"error": ...})
│   │
│   │   🎯 Responsabilidad:
│   │   - Recibir requests HTTP
│   │   - Validar formato (NO reglas de negocio)
│   │   - Invocar casos de uso
│   │
│   ├── application/  🟩 CAPA DE APLICACIÓN (Use Cases)
│   │   └── use_cases/
│   │       ├── uc1_login.py .. uc10_quitar_rol.py
│   │   💬 10 casos de uso (UC1..UC10)
│   │
│   │   🎯 Responsabilidad:
│   │   - Orquestar la lógica de negocio
│   │   - Coordinar servicios del dominio
│   │   - Usar repositorios (a través de puertos)
│   │   - NO depende de infraestructura concreta
│   │
│   ├── domain/  🟥 CAPA DE DOMINIO (Core del negocio)
│   │
│   │   ├── models/
│   │   │   ├── usuario.py
│   │   │   ├── rol.py
│   │   │   └── estado_usuario.py
│   │   │   💬 Entidades y modelos del dominio (reglas puras, dataclasses)
│   │   │
│   │   ├── services/
│   │   │   ├── validacion.py
│   │   │   ├── normalizacion.py
│   │   │   └── auth_service.py       ← creacion/verificacion de credenciales y autorización
│   │   │   💬 Lógica de negocio compleja desacoplada de entidades
│   │   │
│   │   ├── ports/
│   │   │   ├── usuario/
│   │   │   │   ├── usuario_command_port.py
│   │   │   │   └── usuario_query_port.py
│   │   │   ├── rol/
│   │   │   │   ├── rol_command_port.py
│   │   │   │   └── rol_query_port.py
│   │   │   └── authentication/
│   │   │       ├── password_hasher_port.py
│   │   │       ├── token_provider_port.py
│   │   │       └── estado_usuario_cache_port.py
│   │   │   💬 Interfaces (contratos) → patrón Ports & Adapters
│   │   │
│   │   ├── exceptions.py
│   │   │   💬 Excepciones propias del dominio
│   │
│   │   🎯 Responsabilidad:
│   │   - Contener las reglas de negocio
│   │   - Ser independiente de frameworks (ni bcrypt, ni PyJWT)
│   │   - Definir contratos (ports)
│   │
│   ├── infrastructure/  🟨 CAPA DE INFRAESTRUCTURA (Adapters)
│   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │   💬 Configuración global (env, settings)
│   │   │
│   │   ├── auth/
│   │   │   ├── password_hasher.py      ← bcrypt
│   │   │   └── jwt_token_provider.py   ← PyJWT
│   │   │   💬 Adapters de hashing y tokens
│   │   │
│   │   ├── cache/
│   │   │   └── estado_usuario_cache_memoria.py
│   │   │   💬 Cache TTL in-memory del estado del usuario autenticado (patrón híbrido)
│   │   │
│   │   ├── database/
│   │   │   ├── connection.py
│   │   │   │   💬 Conexión async a PostgreSQL (get_db con commit automático)
│   │   │   ├── orm_models/
│   │   │   │   ├── usuario_orm.py
│   │   │   │   └── rol_orm.py          ← incluye tabla usuario_roles
│   │   │   │   💬 Modelos ORM (SQLAlchemy)
│   │   │   ├── repositories/
│   │   │   │   ├── usuario_command_repository.py
│   │   │   │   ├── usuario_query_repository.py
│   │   │   │   ├── rol_command_repository.py
│   │   │   │   └── rol_query_repository.py
│   │   │   │   💬 Implementaciones de los ports (Adapters)
│   │   │   ├── seed.py             ← datos iniciales (ADMIN, USUARIO)
│   │   │   └── seed_runner.py      ← script para ejecutar el seed
│   │   │   💬 Datos iniciales para la BD
│   │   │
│   │   ├── dependencies/
│   │   │   ├── dependency_injection.py
│   │   │   └── auth_dependencies.py   ← get_current_user, require_roles, require_mismo_usuario_o_admin
│   │   │   💬 Inyección de dependencias (wiring de la app)
│   │
│   │   🎯 Responsabilidad:
│   │   - Implementar detalles técnicos (DB, hashing, JWT)
│   │   - Adaptar interfaces del dominio
│   │   - NO contener lógica de negocio
│   │
│   └── requirements.txt
│
├── docs/  📚 Documentación
│   ├── estado_actual_proyecto.md   ← foto del estado actual (fuente de verdad)
│   ├── plan_implementacion.md      ← plan por fases
│   ├── vitacora_agentica.md        ← historial append-only
│   ├── 01_global/                  ← visión, alcance, actores, reglas de negocio
│   ├── 02_tecnico/                 ← decisiones técnicas, modelo de datos y diagramas (puml + svg)
│   ├── 03_procesos/                ← DoR y checklist de listo-para-merge
│   ├── 04_historias_usuario/       ← HU-01..HU-10 (5 archivos c/u)
│   ├── 05_metodologia_agil/        ← metodología Kanban con IA
│   └── 06_auditorias/              ← auditoría de HUs vs código
│
├── tests/  🧪 TESTING
│   ├── conftest.py   ← aísla los tests de DATABASE_URL (valor por defecto)
│   ├── unit/domian/services/        ← heredado de api_normalizacion_afiliados
│   │   ├── test_uc1_login.py .. test_uc10_quitar_rol.py
│   │   ├── test_validacion.py
│   │   ├── test_normalizacion.py
│   │   └── test_auth_service.py
│   │   💬 75 tests unitarios con fakes (sin BD)
│   └── integration/
│       ├── test_flujo_completo.py
│       └── test_autorizacion_roles.py
│       💬 13 tests de integración contra BD real (requieren .env + Postgres con seed)
│
├── AGENTS.md
│   💬 Reglas y convenciones del proyecto para agentes
│
├── README.md
│   💬 Documentación principal del proyecto
│
├── alembic.ini
│   💬 Configuración de migraciones
│
├── Dockerfile
├── docker-entrypoint.sh
├── .dockerignore
│   💬 Despliegue en contenedor (`docker build -t api-usuario-roles .`)
│
├── .env.example
│   💬 Variables de entorno de ejemplo
│
└── pyproject.toml
    💬 Configuración de linting/formato (ruff, black)
```

---

## 🧠 Resumen de Arquitectura

```
Presentation (FastAPI)
        ↓
Application (Use Cases)
        ↓
Domain (Entities + Rules + Ports)
        ↓
Infrastructure (DB, bcrypt, JWT, Cache)
```

### Patrón híbrido de autorización

- **JWT corto (15 min)** con identidad: `sub` (id) + `roles`, firmado HS256.
- Cada request protegido resuelve el **estado real** (activo + roles) desde un cache TTL (60 s) o desde la BD en cache miss.
- Cambios de rol/baja lógica se **revocan en caliente**: se invalida el cache y el próximo request ya ve el nuevo estado, sin esperar la expiración del token.
- Matriz de protección: endpoints de listado/baja/asignar-quitar rol y `/roles/*` exigen `ADMIN`; `GET/PATCH /usuarios/{id}` exigen ser el propio usuario o `ADMIN`.

---

## 🎯 Principios Aplicados

* ✔️ Separación de responsabilidades
* ✔️ Inversión de dependencias (DIP)
* ✔️ Arquitectura Hexagonal (Ports & Adapters)
* ✔️ Dominio desacoplado de frameworks (dominio puro estricto)
* ✔️ Inyección de dependencias con `Depends` (nunca adapters instanciados en use cases)
* ✔️ Código testeable y mantenible

---

## 🚀 Instalación y configuración
```bash
# Clonar el repo
git clone ...

# Crear entorno virtual
python -m venv venv

# Linux
source venv/bin/activate

# Instalar dependencias (requirements.txt está dentro de app/)
pip install -r app/requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con DATABASE_URL real y JWT_SECRET_KEY segura

# Correr migraciones (Alembic ya está inicializado, NO ejecutar `alembic init`)
alembic revision --autogenerate -m "descripcion"
alembic upgrade head

# Seed de roles iniciales (ADMIN y USUARIO)
python -m app.infrastructure.database.seed_runner

# Levantar la API
uvicorn app.main:app --reload
```
---

## 🧪 Testing

```bash
# Tests unitarios (puros, con fakes, sin BD) — 75 tests
pytest

# Tests de integración (requieren .env + PostgreSQL con seed) — 13 tests
python -m pytest tests/integration/

# Lint y formato
venv/bin/ruff check .
venv/bin/black --check .
```

---

## ✅ Estado del proyecto

✔ **Fase 1 — Andamiaje:** COMPLETADA  
Clean Architecture + Hexagonal (Ports & Adapters), SQLAlchemy 2.0 async, DI con `Depends`, 10 casos de uso (UC1..UC10), adapters de auth (bcrypt/PyJWT), routers, handlers y seed de roles.

✔ **Fase 2 — Base de datos real:** COMPLETADA  
Migración inicial de Alembic (`9378f376749f_crear_tablas_usuarios_roles.py`), `alembic upgrade head` y seed ejecutados contra PostgreSQL real.

✔ **Fase 3 — Tests unitarios UC2..UC10:** COMPLETADA  
75 tests con fakes (dominio + presentación).

✔ **Fase 4 — Test de integración real:** COMPLETADA  
13 tests contra BD real (flujo completo + autorización por rol).

✔ **Fase 5 — Autorización por rol:** COMPLETADA  
Patrón híbrido JWT + cache TTL, `require_roles("ADMIN")`, `require_mismo_usuario_o_admin`, revocación en caliente.

Fase 6 — Cierre: **COMPLETADA**  
Documentación integral + auditoría de HUs. Tag **`v1.4.0`**. `main` **actualizado** con todo `develop` (contenedorización + docs) en el merge `0022860` (15/09).

Contenedorización: **COMPLETADA** (post-cierre, 15/09)  
`Dockerfile` + `docker-entrypoint.sh` + `.dockerignore` (`7a8e646`); build con `docker build -t api-usuario-roles .`.

📄 Ver detalle en: `docs/plan_implementacion.md` y `docs/estado_actual_proyecto.md`.

---

## 🗺️ Roadmap

- Fase 1: Andamiaje ✔
- Fase 2: Base de datos real (migración + seed + prueba real) ✔
- Fase 3: Tests unitarios UC2..UC10 con fakes ✔
- Fase 4: Test de integración real ✔
- Fase 5: Autorización por rol (patrón híbrido + revocación) ✔
- Fase 6: Cierre (documentación + auditoría) ✔
- Contenedorización (post-cierre): Dockerfile + entrypoint + `.dockerignore`, `main` actualizado ✔
- Futuro (no bloqueante): release `develop → main` ya realizado · refresh tokens · cache Redis (swap del port `EstadoUsuarioCachePort`)

---

## 🧠 Perfil objetivo

Este proyecto está pensado como material demostrativo para:

- Analista Funcional Jr
- Analista Técnico Funcional
- Primeros roles en proyectos de software administrativo

El foco está puesto en análisis, documentación, trazabilidad y coherencia funcional.

---

## Autor

Emilio Javier Aquino  
Estudiante de Analista de Sistemas

## 📄 Licencia

Proyecto de uso educativo y demostrativo.
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
- Asignar roles a usuarios
- Autorizar endpoints por rol
- Mantener el dominio desacoplado de frameworks (arquitectura limpia)

---

## Documentación funcional

La documentación del proyecto se encuentra en la carpeta `docs/`:

- `estado_actual_proyecto.md` — foto actual del proyecto (fuente de verdad)
- `plan_implementacion.md` — plan por fases (andamiaje → base → autenticación → autorización → cierre)
- `vitacora_agentica.md` — historial cronológico append-only de decisiones

---

## Funcionalidades principales

- Login con emisión de token JWT (`sub` = id de usuario + `roles`)
- Registro de usuarios con contraseña hasheada (bcrypt)
- Listado y consulta de usuarios por ID
- Actualización parcial de usuarios (solo campos presentes, password rehasheada)
- Baja lógica de usuarios (`activo = False`)
- Creación y listado de roles
- Asignación de roles a usuarios (tabla `usuario_roles`)
- Protección de endpoints por JWT y autorización por rol (`require_roles("ADMIN")`)
- Seed de roles iniciales (`ADMIN`, `USUARIO`)

---

## Endpoints principales

| Método | Ruta | Descripción | Protección |
|---|---|---|---|
| GET | `/` | Health check | pública |
| POST | `/auth/login` | Autentica y devuelve token JWT (UC1) | pública |
| GET | `/auth/me` | Usuario autenticado desde el token | JWT |
| POST | `/usuarios/` | Registrar usuario (UC2) | pública* |
| GET | `/usuarios/` | Listar usuarios (UC3) | JWT |
| GET | `/usuarios/{usuario_id}` | Obtener usuario por ID (UC4) | JWT |
| PATCH | `/usuarios/{usuario_id}` | Actualizar usuario (UC5) | JWT |
| DELETE | `/usuarios/{usuario_id}` | Baja lógica (UC6) | JWT |
| POST | `/usuarios/{usuario_id}/roles` | Asignar rol a usuario (UC9) | JWT |
| POST | `/roles/` | Crear rol (UC7) | JWT + ADMIN |
| GET | `/roles/` | Listar roles (UC8) | JWT + ADMIN |

> *`POST /usuarios/` es temporalmente público para permitir el alta inicial; decisión pendiente de cambiarlo a JWT + ADMIN.
>
> Las respuestas de error usan payload uniforme `{"error": "mensaje"}`. Mapeo: 401 (credenciales/token inválido), 403 (rol no autorizado), 404 (no encontrado), 409 (email duplicado), 422 (datos inválidos).

---

## Casos de uso

| UC | Descripción | Estado |
|---|---|---|
| UC1 | Login con JWT | 🟡 parcial — sin migración / BD |
| UC2 | Registrar usuario | 🟡 parcial — sin migración / BD |
| UC3 | Listar usuarios | 🟡 parcial — sin migración / BD |
| UC4 | Obtener usuario por ID | 🟡 parcial — sin migración / BD |
| UC5 | Actualizar usuario | 🟡 parcial — sin migración / BD |
| UC6 | Dar de baja usuario (baja lógica) | 🟡 parcial — sin migración / BD |
| UC7 | Crear rol | 🟡 parcial — sin migración / BD |
| UC8 | Listar roles | 🟡 parcial — sin migración / BD |
| UC9 | Asignar rol a usuario | 🟡 parcial — sin migración / BD |

---

## Arquitectura

El proyecto sigue principios de **Clean Architecture + Hexagonal (Ports & Adapters)**, separando:

- Capa de dominio (entidades puras, servicios y ports)
- Capa de aplicación (casos de uso)
- Capa de infraestructura (adapters: ORM, repositorios, bcrypt, JWT, DI)
- Capa de presentación (routers FastAPI, schemas y handlers)

Esto permite mantener el sistema modular, testeable y desacoplado de frameworks.

---

## Tecnologías utilizadas

- Python 3.13.5
- FastAPI
- SQLAlchemy 2.0 (async) + asyncpg
- PostgreSQL
- Pydantic / pydantic-settings
- bcrypt (hashing de contraseñas)
- PyJWT (emisión y validación de tokens)
- Alembic (migraciones)

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

# 🏗️ Estructura del Proyecto — API Usuario-Roles

Este proyecto implementa una arquitectura basada en **Clean Architecture + Hexagonal (Ports & Adapters)**, separando claramente responsabilidades entre capas.

---

## 📦 Estructura General

```
api_usuario-roles/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│   💬 Migraciones de base de datos (versionado del esquema)
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
│   │       ├── uc1_login.py
│   │       ├── uc2_registrar_usuario.py
│   │       ├── uc3_listar_usuarios.py
│   │       ├── uc4_obtener_usuario_por_id.py
│   │       ├── uc5_actualizar_usuario.py
│   │       ├── uc6_dar_de_baja_usuario.py
│   │       ├── uc7_crear_rol.py
│   │       ├── uc8_listar_roles.py
│   │       └── uc9_asignar_rol.py
│   │   💬 Implementación de casos de uso del sistema
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
│   │   │   └── rol.py
│   │   │   💬 Entidades y modelos del dominio (reglas puras, dataclasses)
│   │   │
│   │   ├── services/
│   │   │   ├── validacion.py
│   │   │   ├── normalizacion.py
│   │   │   └── auth_service.py
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
│   │   │       └── token_provider_port.py
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
│   │   │   └── auth_dependencies.py   ← get_current_user, require_roles
│   │   │   💬 Inyección de dependencias (wiring de la app)
│   │
│   │   🎯 Responsabilidad:
│   │   - Implementar detalles técnicos (DB, hashing, JWT)
│   │   - Adaptar interfaces del dominio
│   │   - NO contener lógica de negocio
│   │
│   └── requirements.txt
│
├── docs/
│   ├── estado_actual_proyecto.md   ← foto del estado actual (fuente de verdad)
│   ├── plan_implementacion.md      ← plan por fases
│   └── vitacora_agentica.md        ← historial append-only
│   💬 Memoria del proyecto
│
├── tests/  🧪 TESTING
│   ├── conftest.py   ← aísla los tests de DATABASE_URL (valor por defecto)
│   └── unit/
│       └── domian/                 ← directorio heredado de api_normalizacion_afiliados
│           └── services/
│               ├── test_validacion.py
│               ├── test_normalizacion.py
│               ├── test_auth_service.py
│               └── test_uc1_login.py   ← tests con fakes (sin BD)
│   💬 Tests unitarios del dominio (in-memory)
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
Infrastructure (DB, bcrypt, JWT)
```

---

## 🎯 Principios Aplicados

* ✔️ Separación de responsabilidades
* ✔️ Inversión de dependencias (DIP)
* ✔️ Arquitectura Hexagonal (Ports & Adapters)
* ✔️ Dominio desacoplado de frameworks (dominio puro estricto)
* ✔️ Inyección de dependencias con `Depends` (nunca adapters instanciados en use cases)
* ✔️ Código testeable y mantenible

---

## 🚀 Beneficios

* Escalable
* Testeable
* Independiente de tecnologías externas
* Fácil de mantener y extender
* Capa de auth reutilizable para otros microservicios

---

## ✅ Estado del proyecto

✔ Fase 1 — Andamiaje: COMPLETADA

Clean Architecture + Hexagonal (Ports & Adapters), SQLAlchemy 2.0 async, DI con `Depends(get_*_ucN)`, 9 casos de uso (UC1..UC9), adapters de auth (bcrypt/PyJWT), routers y seed de roles.

📄 Ver detalle en: `docs/plan_implementacion.md`

⏳ Fase 2 — Base de datos real: PENDIENTE

Crear migración inicial de Alembic, correr `alembic upgrade head` contra PostgreSQL real y ejecutar el seed.

⏳ Fase 3 — Tests unitarios UC2..UC9: PENDIENTE

⏳ Fase 4 — Test de integración real: PENDIENTE

⏳ Fase 5 — Autorización por rol: PENDIENTE

⏳ Fase 6 — Cierre (tag + merge a develop): PENDIENTE

---

## 🗺️ Roadmap

- Fase 1: Andamiaje ✔
- Fase 2: Base de datos real (migración + seed + prueba real) ⏳
- Fase 3: Tests unitarios UC2..UC9 con fakes ⏳
- Fase 4: Test de integración real ⏳
- Fase 5: Autorización por rol (definir roles por endpoint) ⏳
- Fase 6: Cierre (tag `v1.0.0`, merge a develop) ⏳

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
# Documento de Alcance

---

### 1. Descripción general

API REST de **autenticación y autorización (usuarios + roles + JWT)** en Python/FastAPI,
construida con Clean Architecture + Hexagonal (Ports & Adapters). Expone tres grupos de
recursos: **autenticación** (`/auth`), **usuarios** (`/usuarios`) y **roles** (`/roles`),
y protege sus endpoints según una **matriz de roles** decidida con el equipo.

El proyecto documenta además su propio proceso con Historias de Usuario (HU-01..HU-10),
una HU por caso de uso implementado (UC1..UC10), para uso educativo y explicativo.

---

### 2. Funcionalidades incluidas

| Área | Funcionalidad | Caso de uso / HU |
|---|---|---|
| Autenticación | Login con emisión de token JWT | UC1 / HU-01 |
| Autenticación | Obtener el usuario autenticado desde el token (`/auth/me`) | UC1 / HU-01 |
| Usuarios | Registrar usuario con hash de contraseña y autoasignación de rol `USUARIO` | UC2 / HU-02 |
| Usuarios | Listar usuarios | UC3 / HU-03 |
| Usuarios | Obtener un usuario por ID | UC4 / HU-04 |
| Usuarios | Actualizar parcialmente un usuario | UC5 / HU-05 |
| Usuarios | Baja lógica (activar `activo = False`) | UC6 / HU-06 |
| Roles | Crear un rol | UC7 / HU-07 |
| Roles | Listar roles | UC8 / HU-08 |
| Roles | Asignar un rol a un usuario | UC9 / HU-09 |
| Roles | Quitar un rol a un usuario (revocación en caliente) | UC10 / HU-10 |
| Autorización | Matriz de roles por endpoint (ADMIN / propio usuario) | Fase 5 |
| Autorización | Patrón híbrido JWT corto + cache de estado con TTL y revocación en caliente | Fase 5 |
| Operativo | Health check (`GET /`) | — |
| Operativo | Seed de roles iniciales (`ADMIN`, `USUARIO`) | — |

---

### 3. Fuera de alcance

- **Refresh tokens**: hoy solo se emite un access token JWT corto (15 min por defecto).
- **Recuperación de contraseña** por email (verificación de dominio o SMS).
- **Frontend / capa de presentación web**: la API solo expone JSON.
- **Gestión de organización o multi-tenant**: los roles son globales del sistema.
- **Permisos granulares por recurso** más allá de la matriz de roles actual.
- **Cache distribuido (Redis)**: hoy el cache de estado es en memoria (ver limitación en §5).
- **Panel de administración** de usuarios en la propia API.

---

### 4. Límites

- La API autentica contra su **propia base de datos PostgreSQL** (`auth_db`); no consume
  servicios externos de identidad (OAuth/Google/AD).
- La autorización lee el **estado real** del usuario (activo + roles) desde cache/BD, no de
  las claims del token: si el servicio se escala horizontalmente, el cache in-memory debe
  reemplazarse por una solución compartida (ej. Redis) — el port `EstadoUsuarioCachePort`
  ya permite el cambio sin tocar el dominio.
- `POST /usuarios/` (registro) está **público** para permitir el alta inicial; el resto de
  escritura de usuarios/roles exige autenticación y, en general, rol `ADMIN`.

---

### 5. Criterios de aceptación

- Los **88 tests** en verde: 75 unitarios (fakes in-memory) + 13 de integración contra BD real.
- `ruff check .` y `black --check .` sin errores (`pyproject.toml`, line-length 100).
- Migración Alembic aplicada (`9378f376749f_crear_tablas_usuarios_roles`) y seed idempotente
  (`python -m app.infrastructure.database.seed_runner`).
- Matriz de roles verificada por tests de integración (`test_autorizacion_roles.py`):
  403 sin rol, ownership (ADMIN o propio usuario), y **revocación en caliente** de rol/baja con
  token vigente.
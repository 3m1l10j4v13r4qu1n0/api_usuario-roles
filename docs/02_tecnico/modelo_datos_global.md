# Modelo de Datos Global (Entidades Base)

## Entidades lógicas de dominio

### 1. Usuario (`app/domain/models/usuario.py`)
- `id`: int | None — PK, la asigna la BD.
- `nombre_usuario`: str — único, conserva mayúsculas (RN03).
- `email`: str — único, se almacena en minúsculas (RN01).
- `password_hash`: str — hash bcrypt; **nunca se expone** (USR-RN14).
- `nombre_completo`: str | None.
- `activo`: bool — default `True` (baja lógica).
- `fecha_creacion` / `fecha_actualizacion`: datetime | None — las maneja el sistema.
- `ids_roles`: list[int] — relación con `Rol`.

### 2. Rol (`app/domain/models/rol.py`)
- `id`: int | None — PK.
- `nombre`: str — único (ej. `ADMIN`, `USUARIO`).
- `descripcion`: str | None.

### 3. EstadoUsuario (`app/domain/models/estado_usuario.py`) — lógica, no tabla
- `usuario_id`: int, `email`: str, `nombre_usuario`: str, `activo`: bool, `roles`: list[str].
- Es el estado que se cachea por TTL corto para la autorización (patrón híbrido). Se invalida
  al dar de baja (UC6) o cambiar roles (UC9/UC10) para la revocación en caliente.

---

## Tablas físicas (PostgreSQL — migración `9378f376749f_crear_tablas_usuarios_roles`)

### 4. `usuarios`
| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | int | PK, autoincrement |
| `nombre_usuario` | `String(50)` | UNIQUE |
| `email` | `String(255)` | UNIQUE |
| `password_hash` | `String(255)` | — |
| `nombre_completo` | `String(255)` | nullable |
| `activo` | boolean | server_default `true` |
| `fecha_creacion` | datetime | server_default `now()` |
| `fecha_actualizacion` | datetime | server_default + `onupdate` |

### 5. `roles`
| Columna | Tipo | Restricciones |
|---|---|---|
| `id` | int | PK, autoincrement |
| `nombre` | `String(50)` | UNIQUE |
| `descripcion` | `String(255)` | nullable |

### 6. `usuario_roles` (tabla asociativa muchos-a-muchos)
| Columna | Tipo | Restricciones |
|---|---|---|
| `usuario_id` | int | PK compuesta, FK → `usuarios.id` |
| `rol_id` | int | PK compuesta, FK → `roles.id` |

---

## Reglas de Integridad Globales

- Unicidad de `email` y `nombre_usuario` en `usuarios`; unicidad de `nombre` en `roles`.
- Relación **muchos-a-muchos** usuarios ↔ roles vía `usuario_roles` (PK compuesta).
- Los IDs de roles mundo del seed son 1 (`ADMIN`) y 2 (`USUARIO`); el registro autoasigna `USUARIO`.
- Consultas de lectura cargan roles con `selectinload(UsuarioORM.roles)` (evita lazy-load async
  `MissingGreenlet`); escrituras refrescan la relación.
- `UsuarioORM` usa `eager_defaults = True` para recuperar defaults del servidor por `RETURNING`.
- Baja lógica: `activo = False` (nunca `DELETE` físico).
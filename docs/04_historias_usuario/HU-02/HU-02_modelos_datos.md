# HU-02: Modelos de Datos (Registro de usuario)

## Entidades Involucradas

### 1. Usuario
- `id`: int (PK, la asigna la BD)
- `nombre_usuario`: str (únicos, único; conserva mayúsculas — RN03)
- `email`: str (únicos, se guarda en minúsculas — RN01)
- `password_hash`: str (hash bcrypt generado en el alta)
- `nombre_completo`: str | None
- `activo`: bool (default `True`)
- `fecha_creacion`: datetime (server_default now())
- `fecha_actualizacion`: datetime (server_default + onupdate)
- `ids_roles`: list[int] → `[id_rol_USUARIO]` tras el alta

### 2. Rol
- `id`: int (PK)
- `nombre`: str (únicos) — rol buscado por nombre: `USUARIO`
- `descripcion`: str | None

### 3. usuario_roles (tabla asociativa)
- `usuario_id`: int (PK compuesta, FK → usuarios.id)
- `rol_id`: int (PK compuesta, FK → roles.id)

## Reglas de Integridad y Base de Datos

- `usuarios.email` y `usuarios.nombre_usuario` son **UNIQUE** (duplicado → 409 en dominio).
- La tabla `usuario_roles` tiene **PK compuesta** y dos FK.
- La creación usa `UsuarioCommandRepository.crear`, que asocia los `RolORM` de `usuario.ids_roles`
  y refresca la relación (evita acceder a roles con `MissingGreenlet`).
- Los campos temporales se asignan por `server_default` y `eager_defaults=True` en `UsuarioORM`
  (se recuperan por `RETURNING`).
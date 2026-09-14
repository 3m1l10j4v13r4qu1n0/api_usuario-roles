# HU-01: Modelos de Datos (Login)

## Entidades Involucradas

### 1. Usuario
- `id`: int (PK, asignada por la BD)
- `nombre_usuario`: str (único)
- `email`: str (único, se almacena en minúsculas — RN01)
- `password_hash`: str (hash bcrypt; nunca se expone)
- `nombre_completo`: str | None
- `activo`: bool (baja lógica)
- `fecha_creacion`: datetime | None
- `fecha_actualizacion`: datetime | None
- `ids_roles`: list[int]

### 2. Rol
- `id`: int (PK)
- `nombre`: str (único, ej. "ADMIN", "USUARIO")
- `descripcion`: str | None

### 3. EstadoUsuario
- `usuario_id`: int
- `email`: str
- `nombre_usuario`: str
- `activo`: bool
- `roles`: list[str]

> `EstadoUsuario` es un **modelo de dominio lógico** (no una tabla): es el estado que se cachea
> por TTL corto para la autorización (patrón híbrido, `app/domain/models/estado_usuario.py`).

## Reglas de Integridad y Base de Datos

- `usuarios.email` y `usuarios.nombre_usuario` son **UNIQUE**.
- `roles.nombre` es **UNIQUE**.
- El login busca por `email` (normalizado a minúsculas) vía `UsuarioQueryRepository.obtener_por_email`.
- Los roles del usuario se resuelven por `ids_roles` con `RolQueryRepository.obtener_nombres_por_ids`.
- El token JWT contendrá `sub = str(id)` y `roles` (claims), pero la autorización re-verifica el
  estado real (USR-RN11).
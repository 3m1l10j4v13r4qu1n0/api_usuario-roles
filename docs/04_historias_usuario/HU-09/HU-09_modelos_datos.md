# HU-09: Modelos de Datos (Asignar rol)

## Entidades Involucradas

### 1. Usuario
- `id` (destino), `ids_roles: list[int]` — se le agrega el rol.

### 2. Rol
- `id` (el rol a asignar), `nombre`, `descripcion`.

### 3. usuario_roles (tabla asociativa)
- `usuario_id`, `rol_id` (PK compuesta) — se inserta una fila `(usuario_id, rol_id)`.

### 4. EstadoUsuario (cache)
- Se **invalida** la entrada del usuario para reflejar el nuevo rol en el próximo request.

## Reglas de Integridad y Base de Datos

- `asignar_rol` en `UsuarioCommandRepository` agrega el `RolORM` a `usuario.roles` (relación M2M)
  y refresca la relación.
- PK compuesta de `usuario_roles` impide asignar el mismo rol dos veces (las PK se insertan una vez).
- Si el rol ya está asignado, la FK/PK evita duplicados (alto del request con error de integridad).
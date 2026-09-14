# HU-10: Modelos de Datos (Quitar rol)

## Entidades Involucradas

### 1. Usuario
- `id` (destino), `ids_roles: list[int]` — se le quita el rol.

### 2. Rol
- `id` (el rol a quitar), `nombre`, `descripcion`.

### 3. usuario_roles (tabla asociativa)
- `usuario_id`, `rol_id` (PK compuesta) — se elimina la fila `(usuario_id, rol_id)`.

### 4. EstadoUsuario (cache)
- Se **invalida** la entrada del usuario para reflejar la revocación en el próximo request.

## Reglas de Integridad y Base de Datos

- `quitar_rol` en `UsuarioCommandRepository` remueve el `RolORM` de `usuario.roles` (relación M2M)
  y refresca la relación.
- Si el usuario no tenía el rol, el método no falla: la relación simplemente no lo contenía.
- La invalidación de cache cubre tanto UC9 (asignar) como UC10 (quitar) y UC6 (baja).
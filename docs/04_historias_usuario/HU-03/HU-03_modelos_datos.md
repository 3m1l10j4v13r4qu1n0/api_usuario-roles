# HU-03: Modelos de Datos (Listar usuarios)

## Entidades Involucradas

### 1. Usuario
- `id`, `nombre_usuario`, `email`, `password_hash` (no se expone), `nombre_completo`,
  `activo`, `fecha_creacion`, `fecha_actualizacion`, `ids_roles`.

### 2. Rol
- `id`, `nombre`, `descripcion` — referenciado desde `ids_roles`.

### 3. usuario_roles (tabla asociativa)
- `usuario_id`, `rol_id` (PK compuesta).

## Reglas de Integridad y Base de Datos

- La consulta usa `UsuarioQueryRepository.listar` con `selectinload(UsuarioORM.roles)` para
  resolver los roles sin problemas de lazy-load en SQLAlchemy async.
- La salida mapea `usuario.roles` → `ids_roles` (lista de ids) y nunca incluye `password_hash`.
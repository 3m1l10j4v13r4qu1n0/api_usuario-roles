# HU-04: Modelos de Datos (Obtener usuario por ID)

## Entidades Involucradas

### 1. Usuario
- `id` (clave de búsqueda del caso de uso), `nombre_usuario`, `email`, `password_hash`
  (no se expone), `nombre_completo`, `activo`, `fecha_creacion`, `fecha_actualizacion`, `ids_roles`.

### 2. Rol
- Referenciado desde `ids_roles` → se mapea a la lista de ids.

## Reglas de Integridad y Base de Datos

- Búsqueda por PK con `UsuarioQueryRepository.obtener_por_id` (usa `selectinload(UsuarioORM.roles)`).
- El mapper `_usuario_orm_a_entidad` convierte `roles` → `ids_roles`.
# HU-05: Modelos de Datos (Actualizar usuario)

## Entidades Involucradas

### 1. Usuario
- Campos actualizables: `nombre_usuario`, `email`, `password_hash` (derivado de `password`),
  `nombre_completo`.
- `fecha_actualizacion` se regenera automáticamente (`onupdate=func.now()`).
- `id` es clave de búsqueda; `activo` NO se modifica acá (va por baja lógica, UC6).

## Reglas de Integridad y Base de Datos

- Unicidad de `email`: el UC5 usa `buscar_por_email_excluyendo_id(email, usuario_id)` para evitar
  un falso duplicado al mantener el propio email.
- Unicidad de `nombre_usuario` (constraint de BD; el dominio no lo valida explícitamente hoy).
- La actualización usa `UsuarioCommandRepository.actualizar` (setattr por campo) y refresca la
  relación de roles (`_refresh_con_roles`).
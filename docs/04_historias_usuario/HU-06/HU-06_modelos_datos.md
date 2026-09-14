# HU-06: Modelos de Datos (Baja lógica de usuario)

## Entidades Involucradas

### 1. Usuario
- `activo`: bool — se setea a `False` (default `True`).
- `id`: int — clave de búsqueda.
- `fecha_actualizacion` se regenera con el update.

### 2. EstadoUsuario (cache — patrón híbrido)
- `usuario_id`, `email`, `nombre_usuario`, `activo`, `roles`.
- La baja **invalida** la entrada en cache.

## Reglas de Integridad y Base de Datos

- `dar_de_baja` en `UsuarioCommandRepository` hace un UPDATE de `activo = False` y refresca la
  relación de roles.
- La integridad física no cambia: la fila existe, solo se marca inactiva.
- La invalidación de cache no es persistente (TTL 60s por defecto); cargar desde BD es el fallback.
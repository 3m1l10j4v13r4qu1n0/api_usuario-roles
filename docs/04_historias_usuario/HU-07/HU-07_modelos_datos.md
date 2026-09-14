# HU-07: Modelos de Datos (Crear rol)

## Entidades Involucradas

### 1. Rol
- `nombre`: str (obligatorio, único, normalizado RN02)
- `descripcion`: str | None
- `id`: int (PK, la asigna la BD)

## Reglas de Integridad y Base de Datos

- `roles.nombre` es **UNIQUE** (constraint + validación en dominio por `buscar_por_nombre`).
- La creación usa `RolCommandRepository.crear`.
- Los roles seed (`ADMIN`, `USUARIO`) no se duplican: el seed es idempotente
  (`cargar_si_vacia`).
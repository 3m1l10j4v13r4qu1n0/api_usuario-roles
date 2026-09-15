# HU-08: Modelos de Datos (Listar roles)

## Entidades Involucradas

### 1. Rol
- `id`, `nombre`, `descripcion`.

## Reglas de Integridad y Base de Datos

- Consulta simple: `RolQueryRepository.listar` (sin joins).
- `roles.nombre` es único; los roles no seed creados por UC7 se listan igual.
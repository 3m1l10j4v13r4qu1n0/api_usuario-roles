# HU-03: Especificación de API (Listar usuarios)

## Endpoint: Listar usuarios — `GET /usuarios/`

- **Ruta:** `/usuarios/`
- **Método:** GET
- **Protección:** JWT + `require_roles("ADMIN")`
- **Descripción:** Lista todos los usuarios (UC3).

**Respuesta éxito — 200** (`list[UsuarioResponse]`):
```json
[
  {
    "id": 1,
    "nombre_usuario": "admin_bootstrap",
    "email": "admin@bootstrap.com",
    "nombre_completo": null,
    "activo": true,
    "fecha_creacion": "2026-09-14T00:00:00",
    "ids_roles": [1]
  }
]
```

**Respuestas error:**
- `403` → `{"error": "No tiene permisos para realizar esta acción"}` — token válido pero sin rol ADMIN.
- `401` → `{"error": "Token inválido o vencido"}` — sin token o token inválido.

## Campos
- esquema de salida: `UsuarioResponse` (`app/presentation/schemas/usuario_schema.py`).

## Notas
- No permite paginación/filtros en la versión actual.
# HU-08: Especificación de API (Listar roles)

## Endpoint: Listar roles — `GET /roles/`

- **Ruta:** `/roles/`
- **Método:** GET
- **Protección:** JWT + `require_roles("ADMIN")`
- **Descripción:** Lista todos los roles (UC8).

**Respuesta éxito — 200** (`list[RolResponse]`):
```json
[
  { "id": 1, "nombre": "ADMIN", "descripcion": "Acceso total al sistema" },
  { "id": 2, "nombre": "USUARIO", "descripcion": "Acceso básico al sistema" }
]
```

**Respuestas error:**
- `403` → sin rol ADMIN.
- `401` → token inválido/vencido.

## Notas
- Incluye los roles seed (ADMIN, USUARIO) además de los creados con UC7.
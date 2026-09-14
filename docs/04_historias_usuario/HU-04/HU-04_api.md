# HU-04: Especificación de API (Obtener usuario por ID)

## Endpoint: Obtener usuario — `GET /usuarios/{usuario_id}`

- **Ruta:** `/usuarios/{usuario_id}`
- **Método:** GET
- **Protección:** JWT + `require_mismo_usuario_o_admin`
- **Descripción:** Obtiene un usuario por su ID (UC4). Permite ADMIN o el propio usuario.

**Respuesta éxito — 200** (`UsuarioResponse`):
```json
{
  "id": 7,
  "nombre_usuario": "juanperez",
  "email": "juan.perez@example.com",
  "nombre_completo": "Juan Pérez",
  "activo": true,
  "fecha_creacion": "2026-09-14T00:00:00",
  "ids_roles": [2]
}
```

**Respuestas error:**
- `404` → `{"error": "El usuario 'id=999' no existe"}` (`UsuarioNoEncontradoError`).
- `403` → `{"error": "No tiene permisos para realizar esta acción"}` — otro usuario sin ADMIN.
- `401` → token inválido/vencido, usuario inexistente o inactivo.

## Campos
- esquema de salida: `UsuarioResponse`.

## Notas
- El path param `usuario_id` es `int`; la dependencia `require_mismo_usuario_o_admin` usa ese
  mismo parámetro para comparar ownership.
# HU-05: Especificación de API (Actualizar usuario)

## Endpoint: Actualizar usuario — `PATCH /usuarios/{usuario_id}`

- **Ruta:** `/usuarios/{usuario_id}`
- **Método:** PATCH
- **Protección:** JWT + `require_mismo_usuario_o_admin`
- **Descripción:** Actualiza parcialmente un usuario (UC5). Todos los campos son opcionales.

**Request body (JSON) — `UsuarioUpdate`** (todos opcionales; `password` min 8):
```json
{
  "nombre_completo": "Juan Carlos Pérez"
}
```
Otro ejemplo con cambio de credenciales:
```json
{
  "email": "juan.c@example.com",
  "password": "nuevaclave123"
}
```

**Respuesta éxito — 200** (`UsuarioResponse`):
```json
{
  "id": 7,
  "nombre_usuario": "juanperez",
  "email": "juan.c@example.com",
  "nombre_completo": "Juan Carlos Pérez",
  "activo": true,
  "fecha_creacion": "2026-09-14T00:00:00",
  "ids_roles": [2]
}
```

**Respuestas error:**
- `409` → `{"error": "El email '...' ya está registrado"}` (`EmailDuplicadoError`) si el email lo usa otro usuario.
- `404` → `{"error": "El usuario 'id=999' no existe"}`.
- `422` → email inválido, contraseña corta o campos vacíos.
- `403` → otro usuario sin ADMIN.

## Campos
- esquemas: `UsuarioUpdate` (entrada), `UsuarioResponse` (salida).

## Notas
- Si `password` viene, el caso de uso la convalida (RN06), la hashea y mapea a `password_hash`
  (el campo `password` no se persiste).
- Update por campos presentes: `datos.model_dump(exclude_unset=True)`.
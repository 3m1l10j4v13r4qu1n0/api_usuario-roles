# HU-09: Especificación de API (Asignar rol)

## Endpoint: Asignar rol — `POST /usuarios/{usuario_id}/roles`

- **Ruta:** `/usuarios/{usuario_id}/roles`
- **Método:** POST
- **Protección:** JWT + `require_roles("ADMIN")`
- **Status code éxito:** `200 OK`
- **Descripción:** Asigna un rol a un usuario (UC9) e invalida su estado en cache.

**Request body (JSON) — `AsignarRolRequest`:**
```json
{
  "id_rol": 1
}
```

**Respuesta éxito — 200** (`UsuarioResponse` con el rol agregado):
```json
{
  "id": 7,
  "nombre_usuario": "juanperez",
  "email": "juan.perez@example.com",
  "nombre_completo": null,
  "activo": true,
  "fecha_creacion": "2026-09-14T00:00:00",
  "ids_roles": [2, 1]
}
```

**Respuestas error:**
- `404` → `{"error": "El rol 'id=999' no existe"}` o `{"error": "El usuario 'id=999' no existe"}`.
- `403` → sin rol ADMIN.
- `401` → token inválido/vencido.

## Notas
- La autorización del usuario destino se actualiza en el próximo request gracias a la
  invalidación de cache (revocación en caliente, USR-RN12).
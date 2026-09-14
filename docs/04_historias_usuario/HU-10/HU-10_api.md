# HU-10: Especificación de API (Quitar rol)

## Endpoint: Quitar rol — `DELETE /usuarios/{usuario_id}/roles/{rol_id}`

- **Ruta:** `/usuarios/{usuario_id}/roles/{rol_id}`
- **Método:** DELETE
- **Protección:** JWT + `require_roles("ADMIN")`
- **Status code éxito:** `200 OK`
- **Descripción:** Quita un rol a un usuario (UC10) e invalida su estado en cache.

**Respuesta éxito — 200** (`UsuarioResponse` sin el rol):
```json
{
  "id": 7,
  "nombre_usuario": "juanperez",
  "email": "juan.perez@example.com",
  "nombre_completo": null,
  "activo": true,
  "fecha_creacion": "2026-09-14T00:00:00",
  "ids_roles": [2]
}
```

**Respuestas error:**
- `404` → `{"error": "El rol 'id=999' no existe"}` o `{"error": "El usuario 'id=999' no existe"}`.
- `403` → sin rol ADMIN.
- `401` → token inválido/vencido.

## Notas
- La revocación de los permisos se refleja en el próximo request del usuario (no depende de la
  expiración del JWT) — USR-RN12.
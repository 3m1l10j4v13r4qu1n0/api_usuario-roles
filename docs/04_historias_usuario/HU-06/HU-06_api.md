# HU-06: Especificación de API (Baja lógica de usuario)

## Endpoint: Dar de baja usuario — `DELETE /usuarios/{usuario_id}`

- **Ruta:** `/usuarios/{usuario_id}`
- **Método:** DELETE
- **Protección:** JWT + `require_roles("ADMIN")`
- **Status code éxito:** `200 OK`
- **Descripción:** Baja lógica de un usuario (UC6): marca `activo = False` e invalida su estado en cache.

**Respuesta éxito — 200:**
```json
{
  "id": 7,
  "nombre_usuario": "juanperez",
  "email": "juan.perez@example.com",
  "nombre_completo": null,
  "activo": false,
  "fecha_creacion": "2026-09-14T00:00:00",
  "ids_roles": [2]
}
```

**Respuestas error:**
- `404` → `{"error": "El usuario 'id=999' no existe"}`.
- `403` → sin rol ADMIN.
- `401` → token inválido/vencido.

## Notas
- No borra la fila: la baja es lógica (USR-RN07).
- Invalida `EstadoUsuario` en cache → el próximo request de ese usuario con token vigente recibe 401
  (USR-RN12, verificado por integración).
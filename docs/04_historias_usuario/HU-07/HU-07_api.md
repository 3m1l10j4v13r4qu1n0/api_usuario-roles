# HU-07: Especificación de API (Crear rol)

## Endpoint: Crear rol — `POST /roles/`

- **Ruta:** `/roles/`
- **Método:** POST
- **Protección:** JWT + `require_roles("ADMIN")`
- **Status code éxito:** `201 Created`
- **Descripción:** Crea un rol nuevo (UC7).

**Request body (JSON) — `RolCreate`:**
```json
{
  "nombre": "OPERADOR",
  "descripcion": "Opera trámites del sistema"
}
```
`descripcion` es opcional.

**Respuesta éxito — 201** (`RolResponse`):
```json
{
  "id": 3,
  "nombre": "OPERADOR",
  "descripcion": "Opera trámites del sistema"
}
```

**Respuestas error:**
- `422` → `{"error": "El rol 'OPERADOR' ya existe"}` o `{"error": "El nombre del rol es obligatorio"}`.
- `403` → sin rol ADMIN.
- `401` → token inválido/vencido.

## Campos
- esquemas: `RolCreate` (entrada), `RolResponse` (salida).

## Notas
- La unicidad se valida en dominio por nombre normalizado (RN02): `buscar_por_nombre`.
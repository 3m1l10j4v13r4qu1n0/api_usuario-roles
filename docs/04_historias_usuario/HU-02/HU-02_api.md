# HU-02: Especificación de API (Registro de usuario)

## Endpoint: Registrar usuario — `POST /usuarios/`

- **Ruta:** `/usuarios/`
- **Método:** POST
- **Protección:** Público
- **Status code éxito:** `201 Created`
- **Descripción:** Registra un usuario nuevo (UC2). Hashea la contraseña con bcrypt, normaliza
  email (RN01) y texto (RN02), valida reglas RN04/RN05/RN06 y autoasigna el rol `USUARIO`.

**Request body (JSON) — `UsuarioCreate`:**
```json
{
  "nombre_usuario": "juanperez",
  "email": "juan.perez@example.com",
  "password": "secreto123",
  "nombre_completo": "Juan Pérez"
}
```
`nombre_completo` es opcional. `password` debe tener mínimo 8 caracteres.

**Respuesta éxito — 201** (`UsuarioResponse`, no incluye el hash):
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
- `409` → `{"error": "El email 'juan.perez@example.com' ya está registrado"}` (`EmailDuplicadoError`).
- `422` → `{"error": "El email 'x' no es válido: ..."}` / "La contraseña debe tener al
  menos 8 caracteres" / "El nombre de usuario es obligatorio" (`DatoInvalidoError`).

## Campos
- esquema de entrada: `UsuarioCreate` (`app/presentation/schemas/usuario_schema.py`).
- esquema de salida: `UsuarioResponse` (nunca expone `password_hash` — USR-RN14).

## Notas
- En la BD `roles` el rol `USUARIO` tiene **id 2** por seed (id 1 = ADMIN). El `ids_roles`
  degrade en el JSON puede variar.
- Si el rol `USUARIO` no existiera, el alta no se rompe: el usuario se crea sin roles (USR-RN13).
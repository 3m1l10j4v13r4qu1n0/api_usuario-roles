# HU-01: Especificación de API (Login)

## Endpoint 1: Login — `POST /auth/login`

- **Ruta:** `/auth/login`
- **Método:** POST
- **Protección:** Público
- **Descripción:** Autentica un usuario por email y contraseña y emite un token JWT (UC1). El email se normaliza a minúsculas antes de comparar.

**Request body (JSON):**
```json
{
  "email": "juan.perez@example.com",
  "password": "secreto123"
}
```

**Respuesta éxito — 200:**
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "id": 1,
  "email": "juan.perez@example.com",
  "nombre_usuario": "juanperez",
  "roles": ["USUARIO"]
}
```

**Respuestas error:**
- `401` → `{"error": "Credenciales inválidas"}` — email/contraseña incorrectos o usuario inactivo (mensaje genérico).
- `422` → `{"error": ...}` — email inválido.

## Endpoint 2: Obtener usuario autenticado — `GET /auth/me`

- **Ruta:** `/auth/me`
- **Método:** GET
- **Protección:** JWT (`get_current_user`)
- **Descripción:** Devuelve el usuario autenticado resuelto desde el estado real (activo + roles).

**Respuesta éxito — 200:**
```json
{
  "id": 1,
  "email": "juan.perez@example.com",
  "nombre_usuario": "juanperez",
  "roles": ["USUARIO"]
}
```

**Respuestas error:**
- `401` → `{"error": "Token inválido o vencido"}` — falta el token, es inválido/vencido, el usuario ya no existe o está inactivo.

## Campos
- esquemas: `LoginRequest`, `TokenResponse`, `CurrentUserResponse` (`app/presentation/schemas/auth_schema.py`).

## Notas
- El token JWT lleva `sub` (id), `roles`, `iat` y `exp` (15 min por defecto).
- La autorización no confía en los roles del token: resuelve el estado real desde cache/BD.
# HU-01: Caso de Uso Expandido (Login y obtener usuario autenticado)

**Actor Principal:** Usuario Autenticado / No Autenticado.
**Precondición:** Para el login, el usuario puede no estar autenticado. Para `/auth/me` debe existir un token JWT válido emitido por el sistema.

## Flujo Principal (Éxito) — Login
1. El usuario envía `POST /auth/login` con su email y contraseña.
2. El sistema normaliza el email a minúsculas (RN01).
3. El sistema busca el usuario por email en la BD.
4. El sistema verifica que el usuario exista, esté `activo = True` y que la contraseña coincida con el hash (bcrypt).
5. El sistema resuelve los nombres de los roles del usuario.
6. El sistema emite un token JWT con `sub` (id) y `roles`.
7. El usuario recibe el token y sus datos de sesión.

## Flujo Alternativo 1 — Credenciales incorrectas o usuario inactivo
- En el paso 4, si el usuario no existe, está inactivo o la contraseña no coincide, se lanza `CredencialesInvalidasError` → **401** con mensaje genérico (USR-RN15).

## Flujo Principal (Éxito) — GET /auth/me
1. El cliente envía `GET /auth/me` con `Authorization: Bearer <token>`.
2. El sistema decodifica el token (identidad: `sub`).
3. El sistema resuelve el estado real (activo + roles) desde el cache TTL; si hay miss, lo carga de la BD y lo guarda en cache (patrón híbrido, USR-RN11).
4. El sistema devuelve id, email, nombre_usuario y roles.

## Flujo Alternativo 2 — Token inválido/vencido, usuario inexistente o inactivo
- En los pasos 2‑3, si el token falta/es inválido/vencido, o el usuario ya no existe o está inactivo, se lanza `TokenInvalidoError` → **401**.

## Postcondición
- Login: se obtuvo un token JWT de acceso (expiración 15 min por defecto).
- `/auth/me`: se obtuvo el estado real del usuario autenticado.

## Excepciones
- `CredencialesInvalidasError` → 401.
- `TokenInvalidoError` → 401.
- `DatoInvalidoError` (email mal formado) → 422.
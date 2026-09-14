# HU-03: Caso de Uso Expandido (Listar usuarios)

**Actor Principal:** Administrador (rol `ADMIN`).
**Precondición:** El usuario autenticado posee el rol `ADMIN`.

## Flujo Principal (Éxito)
1. El administrador envía `GET /usuarios/` con su Bearer token.
2. `require_roles("ADMIN")` verifica que el usuario tenga el rol ADMIN (intersección de roles, USR-RN09). Si no, `NoAutorizadoError` → 403.
3. El sistema consulta todos los usuarios cargando sus roles (`selectinload`).
4. El sistema devuelve la lista (vacia si no hay registros).

## Flujo Alternativo — Usuario sin rol ADMIN
- En el paso 2, si el usuario autenticado no tiene ADMIN → **403**.

## Postcondición
- Se devolvió la lista de usuarios con sus roles, sin exposición del hash (USR-RN14).

## Excepciones
- `NoAutorizadoError` → 403.
- `TokenInvalidoError` → 401.
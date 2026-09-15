# HU-08: Caso de Uso Expandido (Listar roles)

**Actor Principal:** Administrador (rol `ADMIN`).
**Precondición:** El administrador posee un token JWT válido.

## Flujo Principal (Éxito)
1. El administrador envía `GET /roles/`.
2. `require_roles("ADMIN")` autoriza (si no → `NoAutorizadoError` → 403).
3. El sistema consulta todos los roles.
4. Se devuelve `200` con la lista (vacía si no hay roles).

## Flujo Alternativo — Sin rol ADMIN
- En el paso 2 → **403**.

## Postcondición
- Se devolvieron todos los roles del sistema.

## Excepciones
- `NoAutorizadoError` → 403.
- `TokenInvalidoError` → 401.
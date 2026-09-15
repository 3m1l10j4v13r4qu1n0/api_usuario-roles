# HU-09: Caso de Uso Expandido (Asignar rol)

**Actor Principal:** Administrador (rol `ADMIN`).
**Precondición:** El administrador posee un token JWT válido.

## Flujo Principal (Éxito)
1. El administrador envía `POST /usuarios/{usuario_id}/roles` con `{"id_rol": N}`.
2. `require_roles("ADMIN")` autoriza (si no → `NoAutorizadoError` → 403).
3. El caso de uso busca el rol por id; si no existe → `RolNoEncontradoError` → 404.
4. El repositorio asigna el rol al usuario; si el usuario no existe → `UsuarioNoEncontradoError` → 404.
5. El caso de uso invalida el estado del usuario en cache.
6. Se devuelve `200` con el usuario actualizado.

## Flujo Alternativo 1 — Rol inexistente
- En el paso 3 → **404**.

## Flujo Alternativo 2 — Usuario inexistente
- En el paso 4 → **404**.

## Flujo Alternativo 3 — Sin rol ADMIN
- En el paso 2 → **403**.

## Flujo Alternativo 4 — Cambio en caliente
- Tras el paso 5, el próximo request del usuario destino resuelve su estado real con el nuevo
  rol (sin re-login) — USR-RN11/RN12.

## Postcondición
- El usuario tiene el rol asignado y la autorización lo refleja sin re-login.

## Excepciones
- `RolNoEncontradoError` → 404.
- `UsuarioNoEncontradoError` → 404.
- `NoAutorizadoError` → 403.
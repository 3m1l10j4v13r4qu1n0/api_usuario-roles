# HU-06: Caso de Uso Expandido (Baja lógica de usuario)

**Actor Principal:** Administrador (rol `ADMIN`).
**Precondición:** El administrador posee un token JWT válido.

## Flujo Principal (Éxito)
1. El administrador envía `DELETE /usuarios/{usuario_id}`.
2. `require_roles("ADMIN")` autoriza (si no → `NoAutorizadoError` → 403).
3. El caso de uso ejecuta `repo.dar_de_baja(usuario_id)` (marca `activo = False`).
4. Si el usuario no existe → `UsuarioNoEncontradoError` → 404.
5. El caso de uso invalida el estado del usuario en cache (`estado_cache.invalidar(usuario_id)`).
6. Se devuelve `200` con el usuario inactivo.

## Flujo Alternativo 1 — Usuario inexistente
- En el paso 4 → **404**.

## Flujo Alternativo 2 — Sin rol ADMIN
- En el paso 2 → **403**.

## Flujo Alternativo 3 — Usuario con token vigente intenta acceder
- Como la baja invalidó el cache, el próximo request de ese usuario resolverá su estado real
  (`activo = False`) y será rechazado con 401 (revocación en caliente, USR-RN12).

## Postcondición
- El usuario quedó con `activo = False`; no puede autenticarse (RN08/USR-RN08) ni usar tokens vigentes.

## Excepciones
- `NoAutorizadoError` → 403.
- `UsuarioNoEncontradoError` → 404.
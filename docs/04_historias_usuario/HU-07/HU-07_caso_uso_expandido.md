# HU-07: Caso de Uso Expandido (Crear rol)

**Actor Principal:** Administrador (rol `ADMIN`).
**Precondición:** El administrador posee un token JWT válido.

## Flujo Principal (Éxito)
1. El administrador envía `POST /roles/` con `nombre` y opcionalmente `descripcion`.
2. `require_roles("ADMIN")` autoriza (si no → `NoAutorizadoError` → 403).
3. El caso de uso normaliza el nombre y la descripción (RN02).
4. Si el nombre es vacío → `DatoInvalidoError` → 422.
5. Se verifica que no exista un rol con ese nombre; si existe → `DatoInvalidoError` → 422.
6. Se crea el rol y se devuelve `201`.

## Flujo Alternativo 1 — Nombre vacío/ausente
- En el paso 4 → **422**.

## Flujo Alternativo 2 — Rol duplicado
- En el paso 5 → **422**.

## Flujo Alternativo 3 — Sin rol ADMIN
- En el paso 2 → **403**.

## Postcondición
- Existe un rol nuevo listo para asignarse (UC9/UC10).

## Excepciones
- `DatoInvalidoError` → 422.
- `NoAutorizadoError` → 403.
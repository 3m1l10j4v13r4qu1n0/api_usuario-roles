# HU-04: Caso de Uso Expandido (Obtener usuario por ID)

**Actor Principal:** Usuario Autenticado (ADMIN o el propietario).
**Precondición:** El solicitante posee un token JWT válido.

## Flujo Principal (Éxito)
1. El cliente envía `GET /usuarios/{usuario_id}` con su token.
2. `require_mismo_usuario_o_admin` resuelve el estado real del usuario autenticado:
   - si tiene rol `ADMIN` → permite;
   - si `usuario_id` == id del token → permite;
   - si no, `NoAutorizadoError` → 403.
3. El caso de uso consulta el usuario por id (cargando roles).
4. El sistema devuelve `200` con los datos.

## Flujo Alternativo 1 — Usuario inexistente
- En el paso 3, si no existe, se lanza `UsuarioNoEncontradoError` → **404**.

## Flujo Alternativo 2 — Sin permisos sobre el recurso
- En el paso 2, si el solicitante no es ADMIN ni el propietario → **403**.

## Postcondición
- Se devolvió el usuario solicitado sin exponer el hash (USR-RN14).

## Excepciones
- `UsuarioNoEncontradoError` → 404.
- `NoAutorizadoError` → 403.
- `TokenInvalidoError` → 401.
# HU-05: Caso de Uso Expandido (Actualizar usuario)

**Actor Principal:** Usuario Autenticado (ADMIN o el propietario).
**Precondición:** El solicitante posee un token JWT válido y permisos sobre el recurso (ADMIN
o mismo `usuario_id`).

## Flujo Principal (Éxito)
1. El cliente envía `PATCH /usuarios/{usuario_id}` con los campos a cambiar.
2. `require_mismo_usuario_o_admin` autoriza (ADMIN o propietario).
3. El caso de uso obtiene solo los campos presentes (`exclude_unset=True`).
4. Si viene `email`: lo normaliza (RN01), lo valida (RN04) y verifica que no lo use otro usuario
   (excluyendo el propio id); si está en uso → `EmailDuplicadoError` → 409.
5. Si viene `password`: valida RN06, hashea y la mapea a `password_hash`.
6. El repositorio actualiza y devuelve el usuario; si no existe → `UsuarioNoEncontradoError` → 404.
7. Se devuelve `200` con el usuario actualizado.

## Flujo Alternativo 1 — Email en uso por otro
- En el paso 4, si el email ya pertenece a otro usuario → **409**.

## Flujo Alternativo 2 — Usuario inexistente
- En el paso 6, si el usuario no existe → **404**.

## Flujo Alternativo 3 — Sin permisos
- En el paso 2, si el solicitante no es ADMIN ni el propietario → **403**.

## Postcondición
- Los campos recibidos quedaron persistidos; el `password_hash` nunca se expone (USR-RN14).

## Excepciones
- `EmailDuplicadoError` → 409.
- `UsuarioNoEncontradoError` → 404.
- `NoAutorizadoError` → 403.
- `DatoInvalidoError` → 422.
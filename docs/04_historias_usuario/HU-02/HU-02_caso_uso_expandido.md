# HU-02: Caso de Uso Expandido (Registro de usuario)

**Actor Principal:** Usuario No Autenticado.
**Precondición:** El usuario no está autenticado; el endpoint es público (permite el alta inicial).

## Flujo Principal (Éxito)
1. El usuario envía `POST /usuarios/` con `nombre_usuario`, `email`, `password` y opcionalmente `nombre_completo`.
2. El sistema normaliza el email a minúsculas (RN01) y el texto (RN02), y conserva las mayúsculas del nombre de usuario (RN03).
3. El sistema valida el email (RN04), el nombre de usuario (RN05) y la contraseña (RN06, mínimo 8).
4. El sistema verifica que el email no esté registrado (busca por email normalizado).
5. El sistema hashea la contraseña (bcrypt).
6. El sistema crea la entidad `Usuario` y, si existe el rol `USUARIO`, le asigna `ids_roles = [id_rol]`.
7. El repositorio persiste el usuario con sus roles y devuelve el usuario con ID y fechas.
8. El usuario recibe `201` con los datos (sin exposer el hash).

## Flujo Alternativo 1 — Email duplicado
- En el paso 4, si el email ya está registrado, se lanza `EmailDuplicadoError` → **409**.

## Flujo Alternativo 2 — Datos inválidos
- En el paso 3, si el email es inválido, un obligatorio viene vacío o la contraseña es corta,
  se lanza `DatoInvalidoError` → **422**.

## Flujo Alternativo 3 — Rol por defecto ausente
- En el paso 6, si el rol `USUARIO` no existe en la BD, el alta continúa y el usuario queda sin roles (USR-RN13).

## Postcondición
- Existe un nuevo usuario `activo = True` con contraseña hasheada y rol `USUARIO` (si el rol existe).

## Excepciones
- `EmailDuplicadoError` → 409.
- `DatoInvalidoError` → 422.
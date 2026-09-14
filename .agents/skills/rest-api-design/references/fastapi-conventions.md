# Aplicación de REST design en este proyecto (FastAPI + Clean Architecture)

> Guía local para aplicar las buenas prácticas del skill a `api_usuario-roles`.
> Fuente de verdad: `app/presentation/routers/*.py`, `app/presentation/schemas/*.py`, `app/presentation/handlers.py`.

## Convenciones vigentes del repo

- **Prefijo**: los routers NO llevan `/api` ni `/v1` (se montan directo). Si en el futuro se versiona, usar URL path versioning (`/api/v1/...`), la opción recomendada por el skill.
- **Recursos**: sustantivos en plural, snake_case en campos: `/usuarios`, `/usuarios/{usuario_id}`, `/roles`. Máx. 2 niveles de anidamiento.
- **Excepción justificada a "no verbs"**: `/auth/login` y `/auth/me` son acciones de autenticación, no CRUD de un recurso.
- **Métodos** (según resource-naming):
  - `GET /usuarios` → listar; `GET /usuarios/{id}` → obtener.
  - `POST /usuarios` → crear; `POST /roles` → crear rol.
  - `PATCH /usuarios/{id}` → actualización parcial (no `PUT`).
  - `DELETE /usuarios/{id}` → baja lógica (200 OK con confirmación, no 204, por decisión actual).
  - `POST /usuarios/{id}/roles` → asignar rol (sub-recurso de asociación).
- **Fechas**: ISO 8601 (`YYYY-MM-DD` para `date`, con hora para timestamps).

## Status codes (mapeo por excepción de dominio → `handlers.py`)

| Excepción | HTTP | Payload |
|---|---|---|
| `UsuarioNoEncontradoError` / `RolNoEncontradoError` | 404 | `{"error": "<mensaje>"}` |
| `EmailDuplicadoError` | 409 | `{"error": "<mensaje>"}` |
| `DatoInvalidoError` | 422 | `{"error": "<mensaje>"}` |
| `CredencialesInvalidasError` / `TokenInvalidoError` | 401 | `{"error": "<mensaje>"}` |
| `NoAutorizadoError` | 403 | `{"error": "<mensaje>"}` |
| Bug/error inesperado | 500 | default de FastAPI |

## Reglas para endpoints nuevos

- ✅ Crea esquemas Pydantic dedicados por endpoint (input vs `*Response`), campos en snake_case, sin exponer el `password_hash` ni datos sensibles.
- ✅ Validá la entrada con el schema (422 automático si falla) y validá el negocio con excepciones de dominio (mapeadas solo en `handlers.py`).
- ✅ Inyectá el caso de uso con `Depends(get_*)` desde `dependency_injection.py`; el router NO instancia adapters ni hace `try/except` de negocio.
- ✅ Endpoints protegidos: inyectá `get_current_user` (JWT) como dependencia; para autorización por rol usá `require_roles(...)`.
- ✅ Respondé con el `status_code` que corresponde (201 al crear, 200 al leer/actualizar/baja, 401/403/404/409/422 según tabla).
- ✅ Si el endpoint lista una colección, agregá filtros y paginación (`page`/`limit`) antes de que la colección crezca (hoy `/usuarios` no pagina).
- ❌ No uses verbos en rutas de CRUD simple (`/getUsuario`, `/createUsuario`).
- ❌ No devuelvas 200 para errores ni varíes el formato de error entre endpoints.
- ❌ No hagas sobre-anidado: `/usuarios/{id}/roles/{id}` — resolver con body en `/usuarios/{id}/roles`.
- ❌ No expongas `password_hash` ni incluyas la contraseña en ningún response.
- ❌ No rompas backward compatibility sin versionar.

## Validación

- Para verificar el contrato de un endpoint nuevo, revisar el OpenAPI autogenerado en `/docs` (FastAPI) y correr la suite:

```bash
./venv/bin/python -m pytest -q
```

- Template de referencia: `templates/endpoint_fastapi.py`.
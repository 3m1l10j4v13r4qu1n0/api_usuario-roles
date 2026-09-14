"""Scaffold de endpoint FastAPI para este proyecto (api_usuario-roles).

Convenciones que sigue el repo (ver AGENTS.md y .agents/rules/reglas-solid.md):
- El router solo delega en el caso de uso inyectado con `Depends(get_*)`.
- La validación de entrada es con schemas Pydantic dedicados (input vs response).
- Errores de negocio se lanzan como excepciones de dominio y se traducen a HTTP
  únicamente en `app/presentation/handlers.py` (nunca try/except en el router).
- Cablear la nueva función `get_*` en `app/infrastructure/dependencies/dependency_injection.py`.
- Endpoints protegidos: inyectar `get_current_user` (JWT) y `require_roles(...)`.

Ejemplo: recurso de ejemplo sobre el recurso `usuarios`.
"""

from app.application.use_cases.ucN_xx import XxUseCase
from fastapi import APIRouter, Depends, status

from app.infrastructure.dependencies.auth_dependencies import get_current_user
from app.infrastructure.dependencies.dependency_injection import get_xx_ucN
from app.presentation.schemas.usuario_schema import UsuarioResponse, XxUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get(
    "/{usuario_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK
)
async def obtener_usuario(
    usuario_id: int,
    uc: XxUseCase = Depends(get_xx_ucN),
    _usuario_actual: dict = Depends(get_current_user),
) -> UsuarioResponse:
    """Obtiene un recurso por id. Errores: 401 (sin token), 404 (UsuarioNoEncontradoError)."""
    return await uc.execute(usuario_id=usuario_id)


@router.patch(
    "/{usuario_id}", response_model=UsuarioResponse, status_code=status.HTTP_200_OK
)
async def actualizar_usuario(
    usuario_id: int,
    payload: XxUpdate,
    uc: XxUseCase = Depends(get_xx_ucN),
    _usuario_actual: dict = Depends(get_current_user),
) -> UsuarioResponse:
    """Actualización parcial. Errores: 401, 404, 409 (EmailDuplicadoError), 422."""
    return await uc.execute(usuario_id=usuario_id, datos=payload)

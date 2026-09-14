from fastapi import APIRouter, Depends, status

from app.application.use_cases.uc7_crear_rol import CrearRolUseCase
from app.application.use_cases.uc8_listar_roles import ListarRolesUseCase
from app.infrastructure.dependencies.auth_dependencies import require_roles
from app.infrastructure.dependencies.dependency_injection import (
    get_crear_rol_uc7,
    get_listar_roles_uc8,
)
from app.presentation.schemas.rol_schema import RolCreate, RolResponse

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RolResponse, status_code=status.HTTP_201_CREATED)
async def crear_rol(
    request: RolCreate,
    uc: CrearRolUseCase = Depends(get_crear_rol_uc7),
    _usuario_actual: dict = Depends(require_roles("ADMIN")),
):
    """Crea un rol (UC7). Requiere autenticación y rol ADMIN."""
    return await uc.execute(request.model_dump())


@router.get("/", response_model=list[RolResponse])
async def listar_roles(
    uc: ListarRolesUseCase = Depends(get_listar_roles_uc8),
    _usuario_actual: dict = Depends(require_roles("ADMIN")),
):
    """Lista todos los roles (UC8). Requiere autenticación y rol ADMIN."""
    return await uc.execute()

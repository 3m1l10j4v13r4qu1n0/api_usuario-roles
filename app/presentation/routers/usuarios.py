from fastapi import APIRouter, Depends, status

from app.application.use_cases.uc2_registrar_usuario import RegistrarUsuarioUseCase
from app.application.use_cases.uc3_listar_usuarios import ListarUsuariosUseCase
from app.application.use_cases.uc4_obtener_usuario_por_id import (
    ObtenerUsuarioPorIdUseCase,
)
from app.application.use_cases.uc5_actualizar_usuario import ActualizarUsuarioUseCase
from app.application.use_cases.uc6_dar_de_baja_usuario import DarDeBajaUsuarioUseCase
from app.application.use_cases.uc9_asignar_rol import AsignarRolUseCase
from app.application.use_cases.uc10_quitar_rol import QuitarRolUseCase
from app.infrastructure.dependencies.auth_dependencies import (
    require_mismo_usuario_o_admin,
    require_roles,
)
from app.infrastructure.dependencies.dependency_injection import (
    get_actualizar_usuario_uc5,
    get_asignar_rol_uc9,
    get_dar_de_baja_usuario_uc6,
    get_listar_usuarios_uc3,
    get_obtener_usuario_por_id_uc4,
    get_quitar_rol_uc10,
    get_registrar_usuario_uc2,
)
from app.presentation.schemas.rol_schema import AsignarRolRequest
from app.presentation.schemas.usuario_schema import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def registrar_usuario(
    request: UsuarioCreate,
    uc: RegistrarUsuarioUseCase = Depends(get_registrar_usuario_uc2),
):
    """Registra un usuario nuevo (UC2). Público: permite el alta inicial."""
    return await uc.execute(request.model_dump())


@router.get("/", response_model=list[UsuarioResponse])
async def listar_usuarios(
    uc: ListarUsuariosUseCase = Depends(get_listar_usuarios_uc3),
    _usuario_actual: dict = Depends(require_roles("ADMIN")),
):
    """Lista todos los usuarios (UC3). Requiere autenticación y rol ADMIN."""
    return await uc.execute()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    uc: ObtenerUsuarioPorIdUseCase = Depends(get_obtener_usuario_por_id_uc4),
    _usuario_actual: dict = Depends(require_mismo_usuario_o_admin),
):
    """Obtiene un usuario por ID (UC4). Requiere ADMIN o ser el propio usuario."""
    return await uc.execute(usuario_id)


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    request: UsuarioUpdate,
    uc: ActualizarUsuarioUseCase = Depends(get_actualizar_usuario_uc5),
    _usuario_actual: dict = Depends(require_mismo_usuario_o_admin),
):
    """Actualiza parcialmente un usuario (UC5). Requiere ADMIN o ser el propio usuario."""
    return await uc.execute(usuario_id, request)


@router.delete("/{usuario_id}", status_code=status.HTTP_200_OK)
async def dar_de_baja_usuario(
    usuario_id: int,
    uc: DarDeBajaUsuarioUseCase = Depends(get_dar_de_baja_usuario_uc6),
    _usuario_actual: dict = Depends(require_roles("ADMIN")),
):
    """Baja lógica de un usuario (UC6). Requiere autenticación y rol ADMIN."""
    return await uc.execute(usuario_id)


@router.post(
    "/{usuario_id}/roles",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
)
async def asignar_rol(
    usuario_id: int,
    request: AsignarRolRequest,
    uc: AsignarRolUseCase = Depends(get_asignar_rol_uc9),
    _usuario_actual: dict = Depends(require_roles("ADMIN")),
):
    """Asigna un rol a un usuario (UC9). Requiere autenticación y rol ADMIN."""
    return await uc.execute(usuario_id, request.id_rol)


@router.delete(
    "/{usuario_id}/roles/{rol_id}",
    response_model=UsuarioResponse,
    status_code=status.HTTP_200_OK,
)
async def quitar_rol(
    usuario_id: int,
    rol_id: int,
    uc: QuitarRolUseCase = Depends(get_quitar_rol_uc10),
    _usuario_actual: dict = Depends(require_roles("ADMIN")),
):
    """Quita un rol a un usuario (UC10). Requiere autenticación y rol ADMIN."""
    return await uc.execute(usuario_id, rol_id)

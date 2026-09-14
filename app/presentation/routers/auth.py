from fastapi import APIRouter, Depends

from app.application.use_cases.uc1_login import LoginUseCase
from app.infrastructure.dependencies.auth_dependencies import get_current_user
from app.infrastructure.dependencies.dependency_injection import get_login_uc1
from app.presentation.schemas.auth_schema import (
    CurrentUserResponse,
    LoginRequest,
    TokenResponse,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    uc: LoginUseCase = Depends(get_login_uc1),
):
    """Autentica al usuario y devuelve un token JWT (UC1)."""
    return await uc.execute(request.email, request.password)


@router.get("/me", response_model=CurrentUserResponse)
async def me(usuario_actual: dict = Depends(get_current_user)):
    """Devuelve el usuario autenticado a partir del token."""
    return usuario_actual

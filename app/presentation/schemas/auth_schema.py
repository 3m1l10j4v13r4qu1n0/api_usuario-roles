from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Entrada de autenticación — UC1"""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Salida del login — UC1"""

    access_token: str
    token_type: str
    id: int
    email: str
    nombre_usuario: str
    roles: list[str]


class CurrentUserResponse(BaseModel):
    """Usuario autenticado (resuelto desde el token JWT)"""

    id: int
    email: str
    nombre_usuario: str
    roles: list[str]

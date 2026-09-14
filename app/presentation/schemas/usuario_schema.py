from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class UsuarioCreate(BaseModel):
    """Entrada de alta de usuario — UC2"""

    nombre_usuario: str
    email: EmailStr
    password: str = Field(min_length=8)
    nombre_completo: str | None = None

    @field_validator("nombre_usuario", "nombre_completo")
    @classmethod
    def no_vacio(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v


class UsuarioUpdate(BaseModel):
    """
    Entrada de actualización — UC5
    Todos los campos opcionales; solo se actualizan los que lleguen.
    """

    nombre_usuario: str | None = None
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    nombre_completo: str | None = None

    @field_validator("nombre_usuario", "nombre_completo")
    @classmethod
    def no_vacio(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v


class UsuarioResponse(BaseModel):
    """Salida hacia el cliente — nunca expone el password_hash"""

    id: int
    nombre_usuario: str
    email: str
    nombre_completo: str | None = None
    activo: bool
    fecha_creacion: datetime | None = None
    ids_roles: list[int] = []

    class Config:
        from_attributes = True  # ← convierte la entidad Usuario (dataclass)

from pydantic import BaseModel, field_validator


class RolCreate(BaseModel):
    """Entrada de alta de rol — UC7"""

    nombre: str
    descripcion: str | None = None

    @field_validator("nombre", "descripcion")
    @classmethod
    def no_vacio(cls, v: str | None) -> str | None:
        if v is not None and not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v


class RolResponse(BaseModel):
    """Salida hacia el cliente"""

    id: int
    nombre: str
    descripcion: str | None = None

    class Config:
        from_attributes = True


class AsignarRolRequest(BaseModel):
    """Asigna un rol a un usuario — UC9"""

    id_rol: int

from datetime import datetime
from typing import ClassVar

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.connection import Base
from app.infrastructure.database.orm_models.rol_orm import RolORM


class UsuarioORM(Base):

    __tablename__ = "usuarios"

    __mapper_args__: ClassVar[dict] = {"eager_defaults": True}

    # Clave primaria
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Datos de acceso
    nombre_usuario: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    # Datos opcionales
    nombre_completo: Mapped[str | None] = mapped_column(String(255))

    # Baja lógica
    activo: Mapped[bool] = mapped_column(default=True, server_default="true")

    # Marcas temporales — se gestionan automáticamente
    fecha_creacion: Mapped[datetime] = mapped_column(server_default=func.now())
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Relación muchos-a-muchos con roles
    roles: Mapped[list[RolORM]] = relationship(
        "RolORM",
        secondary="usuario_roles",
        lazy="selectin",
    )

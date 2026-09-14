from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.infrastructure.database.connection import Base


class UsuarioORM(Base):

    __tablename__ = "usuarios"

    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Datos de acceso
    nombre_usuario = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    # Datos opcionales
    nombre_completo = Column(String(255), nullable=True)

    # Baja lógica
    activo = Column(Boolean, nullable=False, default=True, server_default="true")

    # Marcas temporales — se gestionan automáticamente
    fecha_creacion = Column(DateTime, server_default=func.now(), nullable=False)
    fecha_actualizacion = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relación muchos-a-muchos con roles
    roles = relationship(
        "RolORM",
        secondary="usuario_roles",
        lazy="selectin",
    )

from sqlalchemy import Column, ForeignKey, Integer, String, Table

from app.infrastructure.database.connection import Base

# Tabla asociativa usuarios ↔ roles (muchos-a-muchos)
usuario_roles_table = Table(
    "usuario_roles",
    Base.metadata,
    Column("usuario_id", Integer, ForeignKey("usuarios.id"), primary_key=True),
    Column("rol_id", Integer, ForeignKey("roles.id"), primary_key=True),
)


class RolORM(Base):

    __tablename__ = "roles"

    # Clave primaria
    id = Column(Integer, primary_key=True, autoincrement=True)

    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255), nullable=True)

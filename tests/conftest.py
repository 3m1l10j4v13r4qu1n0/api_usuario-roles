"""
Configuración global de pytest.

Garantiza que los tests de dominio puro no dependan de una variable de
entorno DATABASE_URL real. Al definir un valor por defecto antes de que
se importen los módulos, cualquier import que toque config.py (por
ejemplo al construir fixtures de infraestructura) no falla en ausencia
de un archivo .env.
"""

import os

os.environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://test:test@localhost:5432/test_db"
)

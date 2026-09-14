from abc import ABC, abstractmethod


class PasswordHasherPort(ABC):
    """
    Puerto para el hashing de contraseñas.

    UC2 — Registrar usuario
    UC5 — Actualizar usuario
    """

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """
        Genera el hash seguro de una contraseña en texto plano.
        El hash resultante es lo único que se persiste.
        """
        ...

    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verifica si una contraseña en texto plano corresponde al hash almacenado.
        Devuelve True si coincide, False en caso contrario.
        """
        ...

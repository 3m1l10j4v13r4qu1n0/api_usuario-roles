class UsuarioNoEncontradoError(Exception):
    """El usuario no existe"""

    def __init__(self, identificador):
        self.identificador = identificador
        self.mensaje = f"El usuario '{identificador}' no existe"
        super().__init__(self.mensaje)

    def __str__(self):
        return self.mensaje


class RolNoEncontradoError(Exception):
    """El rol no existe"""

    def __init__(self, identificador):
        self.identificador = identificador
        self.mensaje = f"El rol '{identificador}' no existe"
        super().__init__(self.mensaje)

    def __str__(self):
        return self.mensaje


class DatoInvalidoError(Exception):
    """Los datos son inválidos"""

    def __init__(self, mensaje: str):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return self.mensaje


class EmailDuplicadoError(DatoInvalidoError):
    """Error específico para emails duplicados"""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"El email '{email}' ya está registrado")


class CredencialesInvalidasError(Exception):
    """Email o contraseña inválidos en el login"""

    def __init__(self, mensaje: str = "Credenciales inválidas"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return self.mensaje


class TokenInvalidoError(Exception):
    """Token JWT inválido, vencido o ausente"""

    def __init__(self, mensaje: str = "Token inválido o vencido"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return self.mensaje


class NoAutorizadoError(Exception):
    """El usuario no tiene permisos para la acción"""

    def __init__(self, mensaje: str = "No tiene permisos para realizar esta acción"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

    def __str__(self):
        return self.mensaje

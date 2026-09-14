from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import (
    CredencialesInvalidasError,
    DatoInvalidoError,
    EmailDuplicadoError,
    NoAutorizadoError,
    RolNoEncontradoError,
    TokenInvalidoError,
    UsuarioNoEncontradoError,
)


def registrar_handlers(app: FastAPI):

    @app.exception_handler(UsuarioNoEncontradoError)
    async def usuario_no_encontrado_handler(
        request: Request, exc: UsuarioNoEncontradoError
    ):
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(RolNoEncontradoError)
    async def rol_no_encontrado_handler(request: Request, exc: RolNoEncontradoError):
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.exception_handler(EmailDuplicadoError)
    async def email_duplicado_handler(request: Request, exc: EmailDuplicadoError):
        return JSONResponse(status_code=409, content={"error": str(exc)})

    @app.exception_handler(DatoInvalidoError)
    async def dato_invalido_handler(request: Request, exc: DatoInvalidoError):
        return JSONResponse(status_code=422, content={"error": str(exc)})

    @app.exception_handler(CredencialesInvalidasError)
    async def credenciales_invalidas_handler(
        request: Request, exc: CredencialesInvalidasError
    ):
        return JSONResponse(status_code=401, content={"error": str(exc)})

    @app.exception_handler(TokenInvalidoError)
    async def token_invalido_handler(request: Request, exc: TokenInvalidoError):
        return JSONResponse(status_code=401, content={"error": str(exc)})

    @app.exception_handler(NoAutorizadoError)
    async def no_autorizado_handler(request: Request, exc: NoAutorizadoError):
        return JSONResponse(status_code=403, content={"error": str(exc)})

from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import StatementError

from app.shared.validation_translation import translate_error


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}

    for error in exc.errors():
        field = error["loc"][-1]
        message = translate_error(error)

        errors[field] = message

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "message": "Dados inválidos",
            "fields": errors
        }
    )


async def sql_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, StatementError) and "enum" in str(exc).lower():
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": "valor inválido para um dos campos",
                "fiels": {
                    "role": "Use apenas: admin ou client"
                }
            }
        )

    return JSONResponse(
        status_code=500,
        content={
            "message": "Erro interno no servidor"
        }
    )

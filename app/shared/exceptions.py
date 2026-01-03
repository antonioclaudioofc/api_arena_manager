from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)


class UnathorizedException(AppException):
    def __init__(self, message="Credencias inválidas"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message)


class ForbiddenException(AppException):
    def __init__(self, message="Acesso negado"):
        super().__init__(status.HTTP_403_FORBIDDEN, message)


class NotFoundException(AppException):
    def __init__(self, message="Recurso não encontrado"):
        super().__init__(status.HTTP_404_NOT_FOUND, message)


class BadRequestException(AppException):
    def __init__(self, message="Requisição inválida"):
        super().__init__(status.HTTP_400_BAD_REQUEST, message)


class EmailAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(status.HTTP_409_CONFLICT, "E-mail já cadastrado")


class UsernameAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(status.HTTP_409_CONFLICT, "Username já cadastrado")

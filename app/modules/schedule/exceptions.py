from app.shared.exceptions import AppException


class ConflictException(AppException):
    def __init__(self):
        super().__init__("Conflito de horário detectado")

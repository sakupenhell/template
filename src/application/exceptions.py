class ApplicationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class BadRequestException(ApplicationException): ...


class ConflictException(ApplicationException): ...


class ForbiddenException(ApplicationException): ...


class ServiceUnavailableException(ApplicationException): ...

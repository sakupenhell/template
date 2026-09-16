import logging

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.application.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    ServiceUnavailableException,
)
from src.domain.exceptions import (
    DomainValidationException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from src.entrypoints.http.schemas import ErrorResponseSchema

log = logging.getLogger(__name__)


def _error_response(*, status_code: int, code: str, message: str) -> JSONResponse:
    body = ErrorResponseSchema(code=code, message=message)
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return _error_response(status_code=exc.status_code, code="HTTP_ERROR", message=str(exc.detail))


async def entity_not_found_exception_handler(
    request: Request, exc: EntityNotFoundException
) -> JSONResponse:
    return _error_response(status_code=status.HTTP_404_NOT_FOUND, code="NOT_FOUND", message=exc.message)


async def entity_already_exists_exception_handler(
    request: Request, exc: EntityAlreadyExistsException
) -> JSONResponse:
    return _error_response(status_code=status.HTTP_409_CONFLICT, code="CONFLICT", message=exc.message)


async def domain_validation_exception_handler(
    request: Request, exc: DomainValidationException
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        code="UNPROCESSABLE_ENTITY",
        message=exc.message,
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException) -> JSONResponse:
    return _error_response(status_code=status.HTTP_400_BAD_REQUEST, code="BAD_REQUEST", message=exc.message)


async def conflict_exception_handler(request: Request, exc: ConflictException) -> JSONResponse:
    return _error_response(status_code=status.HTTP_409_CONFLICT, code="CONFLICT", message=exc.message)


async def forbidden_exception_handler(request: Request, exc: ForbiddenException) -> JSONResponse:
    return _error_response(status_code=status.HTTP_403_FORBIDDEN, code="FORBIDDEN", message=exc.message)


async def service_unavailable_exception_handler(
    request: Request, exc: ServiceUnavailableException
) -> JSONResponse:
    return _error_response(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        code="SERVICE_UNAVAILABLE",
        message=exc.message,
    )


async def internal_server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("Unhandled exception", exc_info=exc)
    return _error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        code="INTERNAL_SERVER_ERROR",
        message="Internal server error",
    )

import logging
import re
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Final

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from src.application.exceptions import (
    BadRequestException,
    ConflictException,
    ForbiddenException,
    ServiceUnavailableException,
)
from src.config import Settings
from src.domain.exceptions import (
    DomainValidationException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
)
from src.entrypoints.http.api.router import api_router
from src.entrypoints.http.exception_handlers import (
    bad_request_exception_handler,
    conflict_exception_handler,
    domain_validation_exception_handler,
    entity_already_exists_exception_handler,
    entity_not_found_exception_handler,
    forbidden_exception_handler,
    http_exception_handler,
    internal_server_error_handler,
    service_unavailable_exception_handler,
)
from src.entrypoints.http.health import health_router

log = logging.getLogger(__name__)

ExceptionHandlersType = tuple[tuple[type[Exception], Callable], ...]

EXCEPTION_HANDLERS: Final[ExceptionHandlersType] = (
    (HTTPException, http_exception_handler),
    (EntityNotFoundException, entity_not_found_exception_handler),
    (EntityAlreadyExistsException, entity_already_exists_exception_handler),
    (DomainValidationException, domain_validation_exception_handler),
    (BadRequestException, bad_request_exception_handler),
    (ConflictException, conflict_exception_handler),
    (ForbiddenException, forbidden_exception_handler),
    (ServiceUnavailableException, service_unavailable_exception_handler),
    (Exception, internal_server_error_handler),
)


@dataclass
class RestServiceFactory:
    settings: Settings
    container: AsyncContainer

    def custom_generate_unique_id(self, route: APIRoute) -> str:
        method = sorted(route.methods or ["GET"])[0].lower()
        path = route.path_format.strip("/")
        path = path.replace("/", "_").replace("{", "by_").replace("}", "")
        path = re.sub(r"[^a-zA-Z0-9_]+", "_", path)
        path = re.sub(r"_+", "_", path).strip("_")
        return f"{method}_{path}"

    def create_application(self) -> FastAPI:
        app = FastAPI(
            title=self.settings.app.title,
            version=self.settings.app.version,
            description=self.settings.app.description,
            openapi_url="/docs/openapi.json",
            docs_url="/docs/swagger",
            redoc_url="/docs/redoc",
            lifespan=lifespan,
            generate_unique_id_function=self.custom_generate_unique_id,
        )

        self.set_middlewares(app=app)
        self.set_routes(app=app)
        self.set_exceptions(app=app)
        self.set_dependencies(app=app)

        log.info("REST service app configured")
        return app

    def set_middlewares(self, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def set_routes(self, app: FastAPI) -> None:
        app.include_router(health_router)
        app.include_router(api_router)

    def set_exceptions(self, app: FastAPI) -> None:
        for exception, handler in EXCEPTION_HANDLERS:
            app.add_exception_handler(exception, handler)

    def set_dependencies(self, app: FastAPI) -> None:
        setup_dishka(container=self.container, app=app)

    async def stop(self) -> None:
        await self.container.close()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    container: AsyncContainer = app.state.dishka_container
    await container.close()
    log.info("Dishka container closed")


def create_app(settings: Settings, container: AsyncContainer) -> FastAPI:
    return RestServiceFactory(settings=settings, container=container).create_application()

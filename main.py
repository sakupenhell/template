from robyn import Robyn
from robyn.openapi import OpenAPI, OpenAPIInfo

from src.config import settings

app = Robyn(
    file_object=__file__,
    openapi=OpenAPI(
        info=OpenAPIInfo(
            title=settings.app.title,
            version=settings.app.version,
            description=settings.app.description,
        )
    ),
)


if __name__ == "__main__":
    app.start(_check_port=False)

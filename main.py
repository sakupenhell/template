import uvicorn

from src.bootstrap.di.container import create_container
from src.config import settings
from src.entrypoints.http.bootstrap import create_app

container = create_container()
app = create_app(settings, container)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from logging import getLogger

from fastapi import FastAPI
from uvicorn import run

from app.core import Settings, settings
from app.endpoints import list_of_routes
from app.utils.common import get_hostname

logger = getLogger(__name__)


def bind_routes(application: FastAPI, setting: Settings) -> None:
    for route in list_of_routes:
        application.include_router(route, prefix=setting.PATH_PREFIX)


def get_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        docs_url="/swagger",
        openapi_url="/openapi",
        version="1.0.0",
    )
    bind_routes(application, settings)
    application.state.settings = settings
    return application


app = get_app()


if __name__ == "__main__":
    run(
        "app.main:app",
        host=get_hostname(settings.APP_HOST),
        port=settings.APP_PORT,
        reload=True,
        reload_dirs=["app", "tests"],
        log_level="debug",
    )

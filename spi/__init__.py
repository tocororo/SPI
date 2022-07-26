from fastapi import FastAPI

import spi.routes


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(spi.routes.router)

    from spi.celery import create_celery_app
    app.celery_app = create_celery_app()

    return app

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError

from src import events
from src.exception_handlers import validation_error_handler, custom_http_exception_handler
from src.auth.routers import router as auth_router
# from src.users.routers import router as users_router

from src.public.utils.fastapi_custom import (
    CustomHTTPException,
    CustomOpenAPIGenerator
)


def get_app() -> FastAPI:
    """
    Инициализация и настройка объекта приложения fastapi.
    :return: объект FastAPI
    """
    app = FastAPI()
    app.title = 'Gefest'
    app.description = ''
    app.version = '1.0.0'
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.include_router(router=auth_router)
    # app.include_router(router=users_router)
    app.add_event_handler('startup', events.on_startup)
    app.add_event_handler('shutdown', events.on_shutdown)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['https://gefest-pro.tech', 'http://127.0.0.1:5501', 'http://localhost:3000'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.openapi = CustomOpenAPIGenerator(app)
    return app


app = get_app()

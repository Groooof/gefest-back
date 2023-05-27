from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError

from .service import events
from .service.exception_handlers import validation_error_handler, custom_http_exception_handler
from .auth.routers import router as auth_router
from .refs.routers import router as refs_router
from src.users.routers import router as users_router
from src.candidates.routers import router as candidates_router
from src.departments.routers import router as departments_router
from src.positions.routers import router as positions_router
from src.grades.routers import router as grades_router
from .service.fastapi_custom import (
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
    # app.add_exception_handler(RequestValidationError, validation_error_handler)
    # app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.include_router(router=auth_router)
    app.include_router(router=refs_router)
    app.include_router(router=users_router)
    app.include_router(router=candidates_router)
    app.include_router(router=departments_router)
    app.include_router(router=positions_router)
    app.include_router(router=grades_router)
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

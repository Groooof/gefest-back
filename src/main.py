from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic.error_wrappers import ValidationError

from .service.exception_handlers import validation_error_handler, custom_http_exception_handler
from .departments.routers import router as departments_router
from .interviews.routers import router as interviews_router
from .candidates.routers import router as candidates_router
from .positions.routers import router as positions_router
from .vacancies.routers import router as vacancies_router
from .grades.routers import router as grades_router
from .users.routers import router as users_router
from .refs.routers import router as refs_router
from .auth.routers import router as auth_router
from .service import events
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
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.include_router(router=departments_router, prefix='/api/v1')
    app.include_router(router=candidates_router, prefix='/api/v1')
    app.include_router(router=vacancies_router, prefix='/api/v1')
    app.include_router(router=positions_router, prefix='/api/v1')
    app.include_router(router=interviews_router, prefix='/api/v1')
    app.include_router(router=grades_router, prefix='/api/v1')
    app.include_router(router=users_router, prefix='/api/v1')
    app.include_router(router=refs_router, prefix='/api/v1')
    app.include_router(router=auth_router, prefix='/api/v1')
    app.add_event_handler('shutdown', events.on_shutdown)
    app.add_event_handler('startup', events.on_startup)
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

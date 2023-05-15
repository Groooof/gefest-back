import typing as tp

from fastapi.responses import JSONResponse
from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError

from .public.utils.fastapi_custom import CustomHTTPException
from .public.exceptions import InvalidRequestError
from .public.schemas import Error


async def custom_http_exception_handler(request: Request, exc: CustomHTTPException) -> Response:
    headers = getattr(exc, "headers", None)
    if exc.error is None:
        return Response(status_code=exc.status_code, headers=headers)
    
    response_data = Error(error=exc.error, error_description=exc.error_description)
    
    return JSONResponse(
        response_data.dict(), 
        status_code=exc.status_code, 
        headers=headers
    )


async def validation_error_handler(request: Request, exc: tp.Union[RequestValidationError, ValidationError]):
    return await custom_http_exception_handler(request, InvalidRequestError)

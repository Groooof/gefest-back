from .fastapi_custom import CustomHTTPException


class InvalidRequestError(CustomHTTPException):
    status_code = 400
    error = 'invalid_request'
    error_description = 'Invalid request format'


class InvalidClientError(CustomHTTPException):
    status_code = 400
    error = 'invalid_client'
    error_description = 'Invalid client'
    

class InvalidTokenError(CustomHTTPException):
    status_code = 401
    error = 'invalid_token'
    error_description = 'Invalid token'
    

class ExpiredTokenError(CustomHTTPException):
    status_code = 401
    error = 'expired_token'
    error_description = 'Expired token'

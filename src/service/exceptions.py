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
    

class AccountBlockedError(CustomHTTPException):
    status_code = 401
    error = 'account_blocked'
    error_description = 'Account blocked'
    

class ExpiredTokenError(CustomHTTPException):
    status_code = 401
    error = 'expired_token'
    error_description = 'Expired token'


class AccessDenied(CustomHTTPException):
    status_code = 403
    error = 'access_denied'
    error_description = 'Wrong role'


class AlreadyExists(CustomHTTPException):
    status_code = 409
    error = 'already_exists'
    error_description = 'Resourse already exists'

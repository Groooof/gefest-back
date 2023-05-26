import typing as tp
from uuid import UUID

from pydantic import BaseModel

from ..service.pd_models import user

    
class Create:
    class Request:
        class Body(user.Create):
            ...
                
    class Response:
        class Body(BaseModel):
            id: UUID
                
            
class GetSelfInfo:
    class Response:
        class Body(user.Read):
            ...


class GetUserInfo:
    class Response:
        class Body(user.Read):
            ...


class GetCompanyUsersInfo:
    class Response:
        class Body(BaseModel):
            users: tp.List[user.Read]


class DeleteUser:            
    class Response:
        class Body(BaseModel):
            id: UUID

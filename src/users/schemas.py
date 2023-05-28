from uuid import UUID
import typing as tp

from pydantic import BaseModel

from ..service.pd_models import user

    
class Create:
    class Request:
        class Body(user.Create):
            ...
                
    class Response:
        class Body(BaseModel):
            id: UUID
                
            
class GetSelf:
    class Response:
        class Body(user.Read):
            ...


class GetOne:
    class Response:
        class Body(user.Read):
            ...


class GetList:
    class Response:
        class Body(BaseModel):
            users: tp.List[user.Read]


class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID

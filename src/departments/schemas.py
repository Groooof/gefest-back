from uuid import UUID
import typing as tp

from pydantic import BaseModel

from ..service.pd_models import department


class GetList:
    class Response:
        class Body(BaseModel):
            departments: tp.List[department.Read]
            
            
class Create:
    class Request:
        class Body(department.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID
            
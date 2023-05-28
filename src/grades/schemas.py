from uuid import UUID
import typing as tp

from pydantic import BaseModel

from ..service.pd_models import grade


class GetList:
    class Response:
        class Body(BaseModel):
            grades: tp.List[grade.Read]
            
            
class Create:
    class Request:
        class Body(grade.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID
from uuid import UUID
import typing as tp

from pydantic import BaseModel, Field

from ..service.pd_models import vacancy


class Create:
    class Request:
        class Body(vacancy.Create):
            ...

    class Response:
        class Body(BaseModel):
            id: UUID


class GetOne:
    class Response:
        class Body(vacancy.Read):
            ...


class GetList:
    class Request:
        class Query(vacancy.Filters):
            ...
            
    
    class Response:
        class Body(BaseModel):
            vacancies: tp.List[vacancy.Read] = Field(default_factory=list)
            count: int


class Update:
    class Request:
        class Body(vacancy.Update):
            ...

    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID


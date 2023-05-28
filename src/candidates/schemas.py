from uuid import UUID
import typing as tp

from pydantic import BaseModel, Field

from ..service.pd_models import candidate


class Create:
    class Request:
        class Body(candidate.Create):
            ...

    class Response:
        class Body(BaseModel):
            id: UUID


class GetOne:
    class Response:
        class Body(candidate.Read):
            ...


class GetList:
    class Request:
        class Query(candidate.Filters):
            ...
    
    class Response:
        class Body(BaseModel):
            candidates: tp.List[candidate.Read] = Field(default_factory=list)
            count: int


class Update:
    class Request:
        class Body(candidate.Update):
            ...

    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID

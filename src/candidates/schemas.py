from uuid import UUID
import typing as tp
from datetime import date

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
        class Query(BaseModel):
            date_from: tp.Optional[date]
            date_to: tp.Optional[date]
            position_id: tp.Optional[UUID]
            salary_from: tp.Optional[int]
            salary_to: tp.Optional[int]
            
    
    class Response:
        class Body(BaseModel):
            candidates: tp.List[candidate.Read] = Field(default_factory=list)


class Update:
    class Request:
        class Body(candidate.Update):
            ...

    class Response:
        class Body(BaseModel):
            id: UUID


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


class GetList:
    class Request:
        class Query(BaseModel):
            first_name: tp.Optional[str]
            last_name: tp.Optional[str]
            middle_name: tp.Optional[str]
            position_id: tp.Optional[UUID]
            recruiter_id: tp.Optional[UUID]
            
    
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


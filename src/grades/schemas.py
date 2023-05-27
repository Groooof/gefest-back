from pydantic import BaseModel
import typing as tp
from uuid import UUID

from ..service.pd_models import grade


class GetCompanyGrades:
    class Response:
        class Body(BaseModel):
            departments: tp.List[grade.Read]
            
            
class CreateCompanyGrade:
    class Request:
        class Body(grade.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class DeleteCompanyGrade:
    class Response:
        class Body(BaseModel):
            id: UUID
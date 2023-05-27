from pydantic import BaseModel
from uuid import UUID
import typing as tp

from ..service.pd_models import department


class GetCompanyDepartments:
    class Response:
        class Body(BaseModel):
            departments: tp.List[department.Read]
            
            
class CreateCompanyDepartment:
    class Request:
        class Body(department.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class DeleteCompanyDepartment:
    class Response:
        class Body(BaseModel):
            id: UUID
            
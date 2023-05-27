from pydantic import BaseModel
from uuid import UUID
import typing as tp

from ..service.pd_models import position


class GetCompanyPositions:
    class Response:
        class Body(BaseModel):
            departments: tp.List[position.Read]
            
    
class CreateCompanyPosition:
    class Request:
        class Body(position.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class DeleteCompanyPosition:
    class Response:
        class Body(BaseModel):
            id: UUID        
    
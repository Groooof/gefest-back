from uuid import UUID
import typing as tp

from pydantic import BaseModel

from ..service.pd_models import position


class GetList:
    class Response:
        class Body(BaseModel):
            positions: tp.List[position.Read]
            
    
class Create:
    class Request:
        class Body(position.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID        
    
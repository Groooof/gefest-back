from pydantic import BaseModel
from uuid import UUID
import typing as tp

from ..service.pd_models import interview, interview_stage_result


class GetList:
    class Request:
        class Query(interview.Filters):
            ...
            
    class Response:
        class Body(BaseModel):
            interviews: tp.List[interview.Read]
            
            
class GetStageResultsList:        
    class Response:
        class Body(BaseModel):
            stage_results: tp.List[interview_stage_result.Read]
            
        
class Get:
    class Response:
        class Body(interview.Read):
            ...
          
        
class GetStageResult:
    class Response:
        class Body(interview_stage_result.Read):
            ...              
          
            
class Create:
    class Request:
        class Body(interview.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class CreateStageResult:
    class Request:
        class Body(interview_stage_result.Create):
            ...
            
    class Response:
        class Body(BaseModel):
            id: UUID
            
            
class Delete:
    class Response:
        class Body(BaseModel):
            id: UUID
            
from uuid import UUID
from datetime import datetime, date
import typing as tp

from pydantic import BaseModel, Field

from .department import Read as DepartmentRead
from .position import Read as PositionRead
from .grade import Read as GradeRead


class Read(BaseModel):
    id: UUID
    note: str
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        

class Create(BaseModel):
    note: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "title": "CandidateNoteCreate",
            "example": {
                'note': 'Текст примечания'
            }
        }
    
class Update(BaseModel):
    id: tp.Optional[UUID]
    note: tp.Optional[str]

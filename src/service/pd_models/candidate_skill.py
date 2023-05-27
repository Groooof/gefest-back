from uuid import UUID
import typing as tp
from datetime import datetime

from pydantic import BaseModel

from .skill import Read as SkillRead


class Read(BaseModel):
    id: UUID
    skill: SkillRead
    creator_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True


class Create(BaseModel):
    skill_id: UUID
    
    class Config:
        schema_extra = {
            "title": "CandidateSkillCreate",
            "example": {
                'skill_id': '00000000-0000-0000-0000-000000000012'
            }
        }
        
class Update(BaseModel):
    id: tp.Optional[UUID]
    skill_id: UUID
    
    class Config:
        schema_extra = {
            "title": "CandidateSkillUpdate",
            "example": {
                'id': '00000000-0000-0000-0000-000000000005',
                'skill_id': '00000000-0000-0000-0000-000000000012'
            }
        }

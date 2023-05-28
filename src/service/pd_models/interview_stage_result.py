from uuid import UUID
from datetime import datetime
import typing as tp

from pydantic import BaseModel

from . import (
    interview_stage_ref,
)


class Read(BaseModel):
    id: UUID
    interview_stage_old: interview_stage_ref.Read
    interview_stage_new: interview_stage_ref.Read
    note: str
    creator_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class Create(BaseModel):
    interview_stage_code_old: int
    interview_stage_code_new: int
    note: str

    class Config:
        schema_extra = {
            "title": "InterviewStageResultCreate",
            "example": {
                'interview_stage_code_old': 1,
                'interview_stage_code_new': 4,
                'note': 'Some notes...'
            }
        }

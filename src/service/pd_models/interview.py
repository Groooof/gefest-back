from uuid import UUID
from datetime import datetime, date
import typing as tp

from pydantic import BaseModel, Field

from . import (
    user,
    candidate,
    vacancy,
    position,
    interview_stage_ref,
    department,
    grade,
    adress_ref,
    vacancy_skill,
    skill,
    vacancy_priority_ref
)


class Filters(BaseModel):
    creator_id: tp.Optional[UUID]
    vacancy_id: tp.Optional[UUID]
    candidate_id: tp.Optional[UUID]
    stage_code: tp.Optional[int]
    vacancy_priority_code: tp.Optional[int]
    vacancy_deadline_from: tp.Optional[date]
    vacancy_deadline_to: tp.Optional[date]


class Read(BaseModel):
    id: UUID
    candidate: candidate.Read
    vacancy: vacancy.Read
    stage: interview_stage_ref.Read
    creator: user.Read
    created_at: datetime
    
    class Config:
        orm_mode = True
        

class Create(BaseModel):
    candidate_id: UUID
    vacancy_id: UUID

    class Config:
        schema_extra = {
            "title": "InterviewCreate",
            "example": {
                'candidate_id': '00000000-0000-0000-0000-000000000000',
                'vacancy_id': '00000000-0000-0000-0000-000000000001'
            }
        }

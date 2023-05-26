from uuid import UUID
from datetime import datetime, date
import typing as tp

from pydantic import BaseModel, Field


class Read(BaseModel):
    id: UUID
    position: str
    company: str
    work_from: date
    work_to: tp.Optional[date]
    is_actual: bool
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class Create(BaseModel):
    position: str
    company: str
    work_from: date
    work_to: tp.Optional[date]
    is_actual: tp.Optional[bool] = False
    
    class Config:
        schema_extra = {
            "title": "WorkExpirienceCreate",
            "example": {
                'position': 'Сеньер помидор',
                'company': 'SpaceX',
                'work_from': '2019-01-01',
                'work_to': '2020-03-14',
                'is_actual': False
            }
        }
        
        
class Update(BaseModel):
    position: tp.Optional[str]
    company: tp.Optional[str]
    work_from: tp.Optional[date]
    work_to: tp.Optional[date]
    is_actual: tp.Optional[bool]

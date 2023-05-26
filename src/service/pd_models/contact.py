from uuid import UUID
from datetime import datetime
import typing as tp

from pydantic import BaseModel

from .contact_type import Read as ContactTypeRead


class Read(BaseModel):
    type: ContactTypeRead
    value: str
    is_priority: bool
    creator_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class Create(BaseModel):
    type_code: int
    value: str
    is_priority: tp.Optional[bool] = False
    
    class Config:
        schema_extra = {
            "title": "ContactCreate",
            "example": {
                'type_code': 1,
                'value': '79781112233',
                'is_priority': False
            }
        }


class Update(BaseModel):
    value: tp.Optional[str]
    is_priority: tp.Optional[bool] = False

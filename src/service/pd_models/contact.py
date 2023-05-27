from uuid import UUID
from datetime import datetime
import typing as tp

from pydantic import BaseModel

from .contact_type_ref import Read as ContactTypeRead


class Read(BaseModel):
    id: UUID
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
    id: tp.Optional[UUID]
    type_code: int
    value: tp.Optional[str]
    is_priority: tp.Optional[bool] = False

    class Config:
        schema_extra = {
            "title": "ContactUpdate",
            "example": {
                'id': '00000000-0000-0000-0000-000000000011',
                'type_code': 1,
                'value': '79781112233',
                'is_priority': False
            }
        }
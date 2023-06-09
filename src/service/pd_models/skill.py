from uuid import UUID
import typing as tp

from pydantic import BaseModel


class Read(BaseModel):
    id: UUID
    name: str
    normalized_name: str

    class Config:
        orm_mode = True


class Create(BaseModel):
    name: str
    
    class Config:
        schema_extra = {
            "title": "SkillCreate",
            "example": {
                'name': 'GiT Hub'
            }
        }
        
class Update(BaseModel):
    id: tp.Optional[UUID]
    name: str
    
    class Config:
        schema_extra = {
            "title": "SkillUpdate",
            "example": {
                'id': '00000000-0000-0000-0000-000000000005',
                'name': 'GiT Hub'
            }
        }
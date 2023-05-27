from uuid import UUID
from datetime import datetime
import typing as tp

from pydantic import BaseModel

from .language import Read as LanguageRead
from .language_level import Read as LanguageLevelRead


class Read(BaseModel):
    id: UUID
    language: LanguageRead
    language_level: LanguageLevelRead
    creator_id: UUID
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
class Create(BaseModel):
    language_code: int
    language_level_code: int
    
    class Config:
        schema_extra = {
            "title": "CandidateLanguageCreate",
            "example": {
                'language_code': 2,
                'language_level_code': 4
            }
        }
        
        
class Update(BaseModel):
    id: tp.Optional[UUID]
    language_code: int
    language_level_code: int
    
    class Config:
        schema_extra = {
            "title": "CandidateLanguageUpdate",
            "example": {
                'id': '00000000-0000-0000-0000-000000000005',
                'language_code': 2,
                'language_level_code': 4
            }
        }

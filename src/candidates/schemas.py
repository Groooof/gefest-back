from datetime import datetime, date
from uuid import UUID
import typing as tp

from pydantic import BaseModel, Field


class Candidate(BaseModel):
    position_id: tp.Optional[UUID]
    first_name: str
    last_name: str
    middle_name: tp.Optional[str]
    birth_date: tp.Optional[date]
    min_salary: tp.Optional[int]
    adress_code: tp.Optional[int]
    citizenship_code: tp.Optional[int]
    family_status_code: int
    grade_id: tp.Optional[UUID]
    
    class Config:
        schema_extra = {
            "title": "Candidate",
            "example": {
                'position_id': '00000000-0000-0000-0000-000000000005',
                'first_name': 'Алексей',
                'last_name': 'Дубенко',
                'middle_name': None,
                'birth_date': '2002-02-14',
                'salary_minimum': 75000,
                'adress_code': 33,
                'citizenship_code': 1,
                'family_status_code': 1,
                'grade_id': '00000000-0000-0000-0000-000000000009'
            }
        }
    

class Contact(BaseModel):
    type_code: int
    value: str
    is_priority: tp.Optional[bool] = False
    
    class Config:
        schema_extra = {
            "title": "Contact",
            "example": {
                'type_code': 1,
                'value': '79781112233',
                'is_priority': False
            }
        }
        
    
class Expirience(BaseModel):
    position: str
    company: str
    work_from: date
    work_to: tp.Optional[date]
    is_actual: tp.Optional[bool] = False
    
    class Config:
        schema_extra = {
            "title": "Expirience",
            "example": {
                'position': 'Сеньер помидор',
                'company': 'SpaceX',
                'work_from': '2019-01-01',
                'work_to': '2020-03-14',
                'is_actual': False
            }
        }
    
    
class Language(BaseModel):
    language_code: int
    language_level_code: int
    
    class Config:
        schema_extra = {
            "title": "Language",
            "example": {
                'language_code': 2,
                'language_level_code': 4
            }
        }
    

class NewSkill(BaseModel):
    name: str
    
    class Config:
        schema_extra = {
            "title": "NewSkill",
            "example": {
                'name': 'GiT Hub'
            }
        }
        

class ExistingSkill(BaseModel):
    skill_id: UUID
    
    class Config:
        schema_extra = {
            "title": "ExistingSkill",
            "example": {
                'skill_id': '00000000-0000-0000-0000-000000000012'
            }
        }
    

class Create:
    class Request:
        class Body(BaseModel):
            candidate: Candidate
            contacts: tp.List[Contact] = Field(default_factory=list)
            expiriense: tp.List[Expirience] = Field(default_factory=list)
            languages: tp.List[Language] = Field(default_factory=list)
            notes: tp.List[str] = Field(default_factory=list)
            skills: tp.List[tp.Union[NewSkill, ExistingSkill]] = Field(default_factory=list)

    class Response:
        class Body(BaseModel):
            id: UUID
